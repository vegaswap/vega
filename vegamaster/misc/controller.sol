// SPDX-License-Identifier: MIT

pragma solidity 0.6.12;

// import "hardhat/console.sol"; // TODO: Toggle
import "@openzeppelin/contracts-upgradeable/access/OwnableUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/utils/PausableUpgradeable.sol";
import "@openzeppelin/contracts/token/ERC20/SafeERC20.sol";

contract VestingController is OwnableUpgradeable, PausableUpgradeable {
    using SafeMath for uint256;
    using SafeERC20 for IERC20;

    // data
    mapping(address => VestingSchedule) public vestingSchedules;
    address[] public registeredAddresses;

    /// @dev Address of VEGA_TOKEN contract.
    IERC20 public VEGA_TOKEN;
    address private vestingTokenAddress;

    // TODO: Treasury address
    uint256 private DEFAULT_PERIOD;

    // events
    event VestingScheduleRegistered(
        address registeredAddress,
        uint256 registerTime,
        uint256 endTime,
        uint256 cliffTime,
        uint256 totalAmount
    );

    event VestingScheduleUpdated(
        address registeredAddress,
        uint256 registerTime,
        uint256 endTime,
        uint256 cliffTime,
        uint256 totalAmount
    );

    event Withdrawal(address indexed addr, uint256 amount);

    struct VestingSchedule {
        address registeredAddress;
        //        string name;
        uint256 registerTime;
        uint256 cliffTime;
        uint256 terminalPeriodInMonth;
        uint256 totalAmount;
        bool isAdded; // trick to check if one is added
        // calculated
        uint256 endTime;
        uint256 amountPerTerminalPeriod;
        uint256 totalWithdrawnAmount;
        // bool isConfirmed;
    }

    modifier pastCliffTime(address addr) {
        VestingSchedule storage vestingSchedule = vestingSchedules[addr];
        require(
            block.timestamp > vestingSchedule.cliffTime,
            "VESTING: PAST_CLIFF_TIME"
        );
        _;
    }

    modifier validVestingScheduleTimes(uint256 cliffTime) {
        require(cliffTime >= block.timestamp, "VESTING: CLIFF_>_START");
        _;
    }

    modifier notZeroAddress(address addr) {
        require(addr != address(0), "VESTING: ZERO_ADDRESS");
        _;
    }

    function initialize(address _VEGA_TOKEN_ADDR) public {
        __Ownable_init();
        VEGA_TOKEN = IERC20(_VEGA_TOKEN_ADDR);
        vestingTokenAddress = _VEGA_TOKEN_ADDR;
        DEFAULT_PERIOD = 30 days;
    }

    // util function
    function ceil(uint256 a, uint256 m) private pure returns (uint256) {
        uint256 t = a % m;
        if (t == 0) {
            return a.div(m);
        }
        return (a.add(m.sub(t))).div(m);
    }

    function getEndTime(
        uint256 _cliffTime,
        uint256 _amountPerTerminalPeriod,
        uint256 _totalAmount
    ) internal view returns (uint256) {
        return
            _cliffTime.add(
                DEFAULT_PERIOD.mul(ceil(_totalAmount, _amountPerTerminalPeriod))
            );
    }

    function registerVestingSchedule(
        address _registeredAddress,
        uint256 _cliffTime,
        uint256 _terminalPeriodInMonth,
        uint256 _totalAmount
    )
        public
        onlyOwner
        notZeroAddress(_registeredAddress)
        validVestingScheduleTimes(_cliffTime)
    {
        require(
            vestingSchedules[_registeredAddress].isAdded == false,
            "VESTING: ADDRESS_ALREADY_REGISTERED"
        );
        uint256 amountPerTerminalPeriod;
        if (_terminalPeriodInMonth == 0) {
            // no locking case
            amountPerTerminalPeriod = _totalAmount;
        } else {
            amountPerTerminalPeriod = _totalAmount.div(_terminalPeriodInMonth);
        }
        uint256 endTime = getEndTime(
            _cliffTime,
            amountPerTerminalPeriod,
            _totalAmount
        );
        uint256 registerTime = block.timestamp;

        vestingSchedules[_registeredAddress] = VestingSchedule({
            registeredAddress: _registeredAddress,
            registerTime: registerTime,
            cliffTime: _cliffTime,
            endTime: endTime,
            terminalPeriodInMonth: _terminalPeriodInMonth,
            amountPerTerminalPeriod: amountPerTerminalPeriod,
            totalAmount: _totalAmount,
            totalWithdrawnAmount: 0, // isConfirmed: false,
            isAdded: true
        });

        // keep track in array to loop later
        registeredAddresses.push(_registeredAddress);

        VestingScheduleRegistered(
            _registeredAddress,
            registerTime,
            _cliffTime,
            endTime,
            _totalAmount
        );
    }

    function updateVestingSchedule(
        address _updatedAddress,
        uint256 _cliffTime,
        uint256 _terminalPeriodInMonth,
        uint256 _totalAmount
    )
        public
        onlyOwner
        notZeroAddress(_updatedAddress)
        validVestingScheduleTimes(_cliffTime)
    {
        VestingSchedule storage vestingSchedule = vestingSchedules[
            _updatedAddress
        ];
        require(
            vestingSchedule.isAdded == true,
            "VESTING: INVALID_VESTING_SCHEDULE_ADDRESS"
        );

        uint256 amountPerTerminalPeriod;
        if (_terminalPeriodInMonth == 0) {
            amountPerTerminalPeriod = _totalAmount; // no locking case
        } else {
            amountPerTerminalPeriod = _totalAmount.div(_terminalPeriodInMonth);
        }
        uint256 endTime = getEndTime(
            _cliffTime,
            amountPerTerminalPeriod,
            _totalAmount
        );

        vestingSchedules[_updatedAddress] = VestingSchedule({
            registeredAddress: _updatedAddress,
            registerTime: vestingSchedule.registerTime, // registerTime stays the same
            cliffTime: _cliffTime,
            endTime: endTime,
            terminalPeriodInMonth: _terminalPeriodInMonth,
            amountPerTerminalPeriod: amountPerTerminalPeriod,
            totalAmount: _totalAmount,
            totalWithdrawnAmount: 0, // isConfirmed: false,
            isAdded: true
        });

        VestingScheduleUpdated(
            _updatedAddress,
            vestingSchedule.registerTime,
            _cliffTime,
            endTime,
            _totalAmount
        );
    }

    // All pre checking should be done at caller
    function getVestedAmount(
        uint256 _cliffTime,
        uint256 _endTime,
        uint256 _period,
        uint256 _amountPerTerminalPeriod,
        uint256 _totalAmount
    ) internal view returns (uint256) {
        if (block.timestamp >= _endTime) return _totalAmount;

        // returns 0 if cliffTime is not reached
        if (block.timestamp < _cliffTime) return 0;

        uint256 timeSinceCliff = block.timestamp.sub(_cliffTime);
        uint256 validPeriodCount = timeSinceCliff.div(_period) + 1; // at cliff, one amount is withdrawable
        uint256 potentialReturned = validPeriodCount * _amountPerTerminalPeriod;

        if (potentialReturned > _totalAmount) {
            return _totalAmount;
        }

        return potentialReturned;
    }

    // Call at cliffTime/periodTime to release tokens to tokenholders
    // @dev: we pay for the fee
    // TODO: multi call maybe
    function release() external payable onlyOwner whenNotPaused {
        VestingSchedule storage vestingSchedule;
        uint256 i = 0;
        uint256 newTotalWithdrawn = 0;
        for (i = 0; i < registeredAddresses.length; i++) {
            vestingSchedule = vestingSchedules[registeredAddresses[i]];
            newTotalWithdrawn = _release(vestingSchedule);
            vestingSchedule.totalWithdrawnAmount = newTotalWithdrawn;
        }
    }

    function _release(VestingSchedule memory vestingSchedule)
        internal
        onlyOwner
        returns (uint256)
    {
        // Don't throw error, this is run in a loop
        if (block.timestamp < vestingSchedule.cliffTime) {
            return vestingSchedule.totalWithdrawnAmount;
        }

        if (
            vestingSchedule.totalWithdrawnAmount >= vestingSchedule.totalAmount
        ) {
            return vestingSchedule.totalWithdrawnAmount;
        }

        uint256 vestableAmount = getVestedAmount(
            vestingSchedule.cliffTime,
            vestingSchedule.endTime,
            DEFAULT_PERIOD,
            vestingSchedule.amountPerTerminalPeriod,
            vestingSchedule.totalAmount
        );
        uint256 withdrawableAmount = vestableAmount.sub(
            vestingSchedule.totalWithdrawnAmount
        );

        if (
            vestingSchedule.totalWithdrawnAmount + withdrawableAmount >
            vestingSchedule.totalAmount
        ) {
            withdrawableAmount =
                vestingSchedule.totalAmount -
                vestingSchedule.totalWithdrawnAmount;
        }

        if (withdrawableAmount == 0) {
            return vestingSchedule.totalWithdrawnAmount;
        }
        //        require(withdrawableAmount > 0, "VESTING: NO_MORE_WITHDRAWABLE_TOKENS");

        vestingSchedule.totalWithdrawnAmount =
            vestingSchedule.totalWithdrawnAmount +
            withdrawableAmount;

        // transfer token
        require(
            VEGA_TOKEN.transfer(
                vestingSchedule.registeredAddress,
                withdrawableAmount
            )
        );
        Withdrawal(_msgSender(), withdrawableAmount);
        return vestingSchedule.totalWithdrawnAmount;
    }

    function pause(bool status) public onlyOwner {
        if (status) {
            _pause();
        } else {
            _unpause();
        }
    }
}
