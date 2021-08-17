// SPDX-License-Identifier: MIT
pragma solidity ^0.8.5;

// math relating to vesting schedules
// vesting happens linearly after cliff
// note: due to rounding the last period might vest only small amount of tokens
library VestingMath {
    // a period is 30 days. no calendar math, so vesting can fall on random days in the month
    uint256 public constant DEFAULT_PERIOD = 30 days;

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

    function getEndTime(
        uint256 _cliffTime,
        uint256 _amountPerPeriod,
        uint256 _totalAmount,
        uint256 _period
    ) public pure returns (uint256) {
        return
            _cliffTime + (_period * (ceildiv(_totalAmount, _amountPerPeriod)));
    }

    function getEndTime(
        uint256 _cliffTime,
        uint256 _amountPerPeriod,
        uint256 _totalAmount
    ) public pure returns (uint256) {
        return
            getEndTime(
                _cliffTime,
                _amountPerPeriod,
                _totalAmount,
                DEFAULT_PERIOD
            );
    }

    function getVestedAmountPeriod(
        uint256 blocktime,
        uint256 cliffTime,
        uint256 endTime,
        uint256 amountPerPeriod,
        uint256 totalAmount,
        uint256 period
    ) private pure returns (uint256) {
        if (blocktime >= endTime) return totalAmount;

        // returns 0 if cliffTime is not reached
        if (blocktime < cliffTime) return 0;

        uint256 timeSinceCliff = blocktime - cliffTime;
        uint256 validPeriodCount = timeSinceCliff / period + 1; // at cliff, one amount is withdrawable
        uint256 potentialReturned = validPeriodCount * amountPerPeriod;

        if (potentialReturned > totalAmount) {
            return totalAmount;
        }

        return potentialReturned;
    }

    function getVestedAmount(
        uint256 blocktime,
        uint256 cliffTime,
        uint256 endTime,
        uint256 amountPerPeriod,
        uint256 totalAmount
    ) public pure returns (uint256) {
        return
            getVestedAmountPeriod(
                blocktime,
                cliffTime,
                endTime,
                amountPerPeriod,
                totalAmount,
                DEFAULT_PERIOD
            );
    }
}