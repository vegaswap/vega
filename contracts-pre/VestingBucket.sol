// // SPDX-License-Identifier: MIT
pragma solidity ^0.8.5;

import "./AbstractBucket.sol";
import "./VegaToken.sol";

// bucket with vesting of multiple addresses
// claims and
// claim addresses have claims towards the bucket
// vesting in equal parts per time
// e.g. 6 months, 1/6 equal
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
    uint256 public startTime;
    uint256 public endTime;

    event ClaimAdded(address claimAddress, uint256 claimTotalAmount, uint256 amountPerPeriod);
    event DepositOwner(address indexed addr, uint256 amount);
    event WithdrawClaim(address indexed addr, uint256 amount);
    event WithdrawOwner(uint256 amount);

    uint256 public constant default_period = 30 days;

    constructor(
        address _VEGA_TOKEN_ADDRESS,
        uint256 _cliffTime,
        uint256 _numPeriods,
        uint256 _totalAmount
    ) AbstractBucket(_VEGA_TOKEN_ADDRESS) {
        require(
            _cliffTime >= block.timestamp,
            "VESTINGBUCKET: cliff must be in the future"
        );
        require(_numPeriods > 0, "numPeriods must be larger than 0");
        require(_numPeriods < 25, "numPeriods must be smaller than 25");
        cliffTime = _cliffTime;
        numPeriods = _numPeriods;
        totalAmount = _totalAmount;

        bucketAmountPerPeriod = totalAmount / numPeriods;
        endTime = getEndTime(
            bucketAmountPerPeriod
        );

        uint256 duration = endTime - block.timestamp;
        require (duration < 731 days, "VESTINGBUCKET: don't vest more than 2 years");

        totalWithdrawnAmount = 0;
        totalClaimAmount = 0;
        //start time is deploy time
        startTime = block.timestamp;
    }
    
    // divide a with m and choose higher value if its round
    // a > m
    function ceildiv(uint256 a, uint256 m) public pure returns (uint256) {
        uint256 t = a % m;
        if (t == 0) {
            return a / m;
        } else {
            return (a + (m - t)) / m;
        }
    }

    function linearFrom(uint256 _amountPerPeriod) public view returns (uint256) {
        return (default_period * (ceildiv(totalAmount, _amountPerPeriod)));
    }

    function getEndTime(
        uint256 _amountPerPeriod
    ) public view returns (uint256) {
        return
            cliffTime + linearFrom(_amountPerPeriod);
    }

    function getVestedAmountPeriod(
        uint256 amountPerPeriod
    ) private view returns (uint256) {
        if (block.timestamp >= endTime) return totalAmount;

        // returns 0 if cliffTime is not reached
        if (block.timestamp < cliffTime) return 0;

        uint256 timeSinceCliff = block.timestamp - cliffTime;
        // at cliff, one amount is withdrawable
        uint256 validPeriodCount = 1 + timeSinceCliff / default_period;
        uint256 potentialReturned = validPeriodCount * amountPerPeriod;

        if (potentialReturned > totalAmount) {
            return totalAmount;
        }

        return potentialReturned;
    }

    function depositOwner(uint256 amount) public onlyOwner {
        require(vega_token.allowance(msg.sender, address(this)) >= amount, "not enough allowance");
        bool transferSuccess = vega_token.transferFrom(
            msg.sender,
            address(this),
            amount
        );
        require(transferSuccess, "VESTINGBUCKET: deposit failed");
        emit DepositOwner(msg.sender, amount);
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

        uint256 bal = vega_token.balanceOf(address(this));
        uint256 unclaimed = bal - totalClaimAmount;
        require(_claimTotalAmount <= unclaimed, "VESTINGBUCKET: can not claim tokens that are not deposited");

        uint256 amountPerPeriod = _claimTotalAmount / numPeriods;

        claims[_claimAddress] = Claim({
            claimAddress: _claimAddress,
            amountPerPeriod: amountPerPeriod,
            claimTotalAmount: _claimTotalAmount,
            withdrawnAmount: 0,
            isAdded: true
        });

        emit ClaimAdded(_claimAddress, _claimTotalAmount, amountPerPeriod);

        claimAddresses.push(_claimAddress);
        totalClaimAmount += _claimTotalAmount;
    }

    function getVestableAmount(address _claimAddress)
        public
        view
        returns (uint256)
    {
        Claim memory claim = claims[_claimAddress];
        uint256 vestableAmount = getVestedAmountPeriod(
                claim.amountPerPeriod
            );
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

        uint256 vestableAmount = getVestedAmountPeriod(claim.amountPerPeriod);

        uint256 withdrawAmount = vestableAmount - claim.withdrawnAmount;
        uint256 totalAfterwithdraw = claim.withdrawnAmount + withdrawAmount;
        require(
            totalAfterwithdraw <= claim.claimTotalAmount,
            "VESTINGBUCKET: can not withdraw more than total"
        );

        require(withdrawAmount > 0, "VESTINGBUCKET: no amount claimed");

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
            vestClaimMax(claimAddresses[i]);
        }
    }

    //allow withdraws which are not claimed
    function withdrawOwner(uint256 amount) public onlyRefOwner {
        //transfer any unclaimed balances
        uint256 bucketbalance = vega_token.balanceOf(address(this));
        uint256 unclaimedbalance = bucketbalance - totalClaimAmount;
        bool transferSuccess = vega_token.transfer(msg.sender, unclaimedbalance);
        require(transferSuccess, "VESTINGBUCKET: withdrawOwner failed");
        emit WithdrawOwner(amount);
    }
    
}
