// // SPDX-License-Identifier: MIT
pragma solidity ^0.8.5;

import "./AbstractBucket.sol";
import "./Ownable.sol";
import "./VegaToken.sol";
import "./VestingMath.sol";

//bucket with vesting of multiple addresses
//claims and
//claim addresses have claims towards the bucket
//vesting in equal parts per time
//e.g. 6 months, 1/6 equal
contract VestingBucket is AbstractBucket {
    //a claim towards this bucket by an addreess
    struct Claim {
        address claimAddress;
        uint256 claimTotalAmount;
        uint256 amountPerPeriod;
        uint256 withdrawnAmount;
        bool isAdded;
    }

    mapping(address => Claim) public claims;
    address[] public claimAddresses;
    uint256 public totalClaimAmount;
    uint256 public totalWithdrawnAmount;

    //unix time when vesting starts
    uint256 public cliffTime;
    //how many periods .the number of months not the number of the final month
    uint256 public numPeriods;
    //how much in total is vested
    uint256 public totalAmount;
    // calculated
    //how much per period. since its linear this is calculated
    uint256 public bucketAmountPerPeriod;
    uint256 public endTime;

    //TODO deposit
    //event DepositOwner(address indexed addr, uint256 amount);
    event WithdrawClaim(address indexed addr, uint256 amount);
    event WithdrawOwner(uint256 amount);

    constructor(
        address _VEGA_TOKEN_ADDRESS,
        uint256 _cliffTime,
        uint256 _numPeriods,
        uint256 _totalAmount
    ) AbstractBucket(_VEGA_TOKEN_ADDRESS) {
        require(
            _cliffTime >= block.timestamp,
            "VESTINGBUCKET cliff must be in the future"
        );
        cliffTime = _cliffTime;
        numPeriods = _numPeriods;
        totalAmount = _totalAmount;

        bucketAmountPerPeriod = totalAmount / numPeriods;
        endTime = VestingMath.getEndTime(
            _cliffTime,
            bucketAmountPerPeriod,
            _totalAmount
        );

        totalWithdrawnAmount = 0;
        totalClaimAmount = 0;
    }

    //linear vesting claim
    function addClaim(address _claimAddress, uint256 _claimTotalAmount)
        public
        onlyRefOwner
    {
        if (claims[_claimAddress].isAdded)
            revert("VESTINGBUCKET: claim at this address already exists");

        require(_claimTotalAmount > 0, "VESTINGBUCKET: claim can not be zero");

        require(
            totalClaimAmount + _claimTotalAmount <= totalAmount,
            "VESTINGBUCKET: can not claim more than total"
        );

        //TODO! add prechecks

        uint256 amountPerPeriod = _claimTotalAmount / numPeriods;

        claims[_claimAddress] = Claim({
            claimAddress: _claimAddress,
            amountPerPeriod: amountPerPeriod,
            claimTotalAmount: _claimTotalAmount,
            withdrawnAmount: 0,
            isAdded: true
        });

        claimAddresses.push(_claimAddress);
        totalClaimAmount += _claimTotalAmount;
        //amountPerPeriod: amountPerPeriod
    }

    function getVestedAmount(Claim memory claim) public view returns (uint256) {
        uint256 blocktime = block.timestamp;
        return
            VestingMath.getVestedAmount(
                blocktime,
                cliffTime,
                endTime,
                claim.amountPerPeriod,
                claim.claimTotalAmount
            );
    }

    function getVestableAmount(address _claimAddress)
        public
        view
        returns (uint256)
    {
        Claim memory claim = claims[_claimAddress];
        uint256 vestableAmount = getVestedAmount(claim);
        return vestableAmount;
    }

    //vest the claim. this vests the maximum possible
    function vestClaimMax(address _claimAddress) public {
        require(
            msg.sender == _claimAddress ||
                msg.sender == owner() ||
                msg.sender == refOwner(),
            "VESTINGBUCKET: can only call from claimaddress or owner"
        );

        if (!claims[_claimAddress].isAdded)
            revert("VESTINGBUCKET: claim does not exist");

        Claim storage claim = claims[_claimAddress];

        uint256 vestableAmount = getVestedAmount(claim);

        uint256 withdrawAmount = vestableAmount - claim.withdrawnAmount;
        uint256 totalAfterwithdraw = claim.withdrawnAmount + withdrawAmount;
        require(
            totalAfterwithdraw <= claim.claimTotalAmount,
            "VESTINGBUCKET: can not withdraw more than total"
        );

        require(withdrawAmount > 0, "VESTINGBUCKET: no amount claimed");

        //edge case is handled in vesting math
        //  if (vestingSchedule.totalWithdrawnAmount + withdrawableAmount > vestingSchedule.totalAmount) {
        //   withdrawableAmount = vestingSchedule.totalAmount - vestingSchedule.totalWithdrawnAmount;
        // }

        require(
            vega_token.transfer(_claimAddress, withdrawAmount),
            "VESTINGBUCKET: transfer failed"
        );
        emit WithdrawClaim(claim.claimAddress, withdrawAmount);
        claim.withdrawnAmount += withdrawAmount;
        totalWithdrawnAmount += withdrawAmount;
    }

    //owner calls all claims
    function allClaim() public onlyRefOwner {
        //for every claim
        uint256 i = 0;
        for (i = 0; i < claimAddresses.length; i++) {
            address ca = claimAddresses[i];
            vestClaimMax(ca);
            //uint256 vestableAmount = getVestedAmount(claim);
            //total += vestableAmount;
        }
    }

    //allow withdraws which are not claimed
    function withdrawOwner(uint256 amount) public onlyRefOwner {
        //todo: could add check against existing claims
        bool transferSuccess = vega_token.transfer(msg.sender, amount);
        require(transferSuccess, "VESTINGBUCKET: withdrawOwner failed");
        emit WithdrawOwner(amount);
    }

    //pro forma functions

    //remove claim is not implemented, if there is issues need to use new address
    // function removeClaim(address _claimAddress) public onlyRefOwner {
    //     claims[_claimAddress] = zero
    //     numClaims -= 1;
    // }

    // function depositOwner(uint256 amount) public onlyOwner {
    //     //require(approve)
    //     bool transferSuccess = vega_token.transferFrom(
    //         msg.sender,
    //         address(this),
    //         amount
    //     );
    //     require(transferSuccess, "VESTINGBUCKET: deposit failed");
    //     emit DepositOwner(msg.sender, amount);
    // }
}
