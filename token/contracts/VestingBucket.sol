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
    address refowner;
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
    uint256 totalWithdrawnAmount;

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
    uint256 public numClaims;

    //TODO deposit
    event Withdrawal(address indexed addr, uint256 amount);

    modifier onlyRefOwner() {
        require(msg.sender == refowner, "Ownable: caller is not the owner");
        _;
    }

    constructor(
        address _VEGA_TOKEN_ADDRESS,
        uint256 _cliffTime,
        uint256 _numPeriods,
        uint256 _totalAmount,
        address _refowner
    ) AbstractBucket(_VEGA_TOKEN_ADDRESS) {
        refowner = _refowner;
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
        numClaims = 0;
        //claimAddresses =
    }

    //linear vesting claim
    function addClaim(address _claimAddress, uint256 _claimTotalAmount)
        public
        onlyRefOwner
    {
        if (claims[_claimAddress].isAdded)
            revert("VESTINGBUCKET: claim at this address already exists");

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

        //claimAddresses[numClaims] = _claimAddress;
        claimAddresses.push(_claimAddress);
        totalClaimAmount += _claimTotalAmount;
        numClaims += 1;
        //amountPerPeriod: amountPerPeriod
    }

    function getCurrentTime() public view returns (uint256) {
        return block.timestamp;
    }

    function getVestedAmount(Claim memory claim) public view returns (uint256) {
        uint256 blocktime = block.timestamp;
        return
            VestingMath.getVestedAmountTS(
                blocktime,
                cliffTime,
                endTime,
                claim.amountPerPeriod,
                claim.claimTotalAmount
            );
    }

    function getVestableAmountAll() public view returns (uint256) {
        uint256 blocktime = block.timestamp;

        uint256 amount = VestingMath.getVestedAmountTS(
            blocktime,
            cliffTime,
            endTime,
            bucketAmountPerPeriod,
            totalAmount
        );

        return amount;

        // uint256 total = 0;
        // Claim memory claim;
        // uint256 i = 0;
        // for (i = 0; i < claimAddresses.length; i++) {
        //     //claim = claims[i];
        //     address _ca = claimAddresses[i];
        //     claim = claims[_ca];
        //     uint256 vestableAmount = getVestedAmount(claim);
        //     total += vestableAmount;
        // }

        // return total;
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
    function vestClaimMax(address _claimAddress) public returns (uint256) {
        //BUG! TODO!
        //TODO! throw error String
        //check if claims exists

        //isAdded!
        require(
            msg.sender == _claimAddress || msg.sender == owner(),
            "VESTINGBUCKET: can only call from claimaddress or owner"
        );

        if (!claims[_claimAddress].isAdded)
            revert("VESTINGBUCKET: claim does not exist");

        // require(
        //     claimAddresses[_claimAddress].exists,
        //     "_claimAddress does not exist."
        // );

        Claim memory claim = claims[_claimAddress];

        uint256 vestableAmount = getVestedAmount(claim);

        uint256 withdrawAmount = vestableAmount - claim.withdrawnAmount;
        uint256 willwithdraw = claim.withdrawnAmount + withdrawAmount;
        require(willwithdraw <= claim.claimTotalAmount);

        //TODO! edge case
        //  if (vestingSchedule.totalWithdrawnAmount + withdrawableAmount > vestingSchedule.totalAmount) {
        //   withdrawableAmount = vestingSchedule.totalAmount - vestingSchedule.totalWithdrawnAmount;
        // }

        require(vega_token.transfer(claim.claimAddress, withdrawAmount));
        emit Withdrawal(claim.claimAddress, withdrawAmount);
        claim.withdrawnAmount += withdrawAmount;
        totalWithdrawnAmount += withdrawAmount;
        return withdrawAmount;
    }

    //owner calls all claims
    function allClaim(address _claimAddress) public returns (uint256) {
        require(msg.sender == owner());

        //for every claim
        //Claim memory claim = claims[i];
        //vestClaimMax()
    }

    // function depositOwner() public onlyOwner {

    // }

    // function withdrawOwner(uint256 amount) public onlyOwner {
    //     require(vega_token.transfer(msg.sender, amount));
    // }
}
