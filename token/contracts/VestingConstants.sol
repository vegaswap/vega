// // SPDX-License-Identifier: MIT
pragma solidity ^0.8.5;

library VestingConstants {
    uint256 public constant DEFAULT_PERIOD = 30 days;

    uint256 constant K = 10**3;
    uint256 constant M = 10**6;

    //multiple is 1/price
    uint256 public constant seedMultiple = 125; //0.008$
    uint256 public constant privateMultiple = 100; //0.01$
    uint256 public constant publicMultiple = 84; //0.0119$

    //1000M supply allocate to 11 buckets
    //total amounts, no decimals
    uint256 public constant seedAmount = 12 * M + 500 * K;
    uint256 public constant privateAmount = 65 * M;
    uint256 public constant publicAmount = 16 * M + 666 * K + 667;
    uint256 public constant liqAmount = 150 * M;
    uint256 public constant lprewardsAmount = 200 * M;
    uint256 public constant lpgrantsAmount = 50 * M;
    uint256 public constant ecoAmount = 100 * M;
    uint256 public constant trademiningAmount = 200 * M;
    uint256 public constant teamAmount = 150 * M;
    uint256 public constant advisoryAmount = 50 * M;
    //treasury is the rest
    uint256 public constant treasuryAmount = 5833333;

    //cliffs
    uint256 public constant seedCliff = 0 days; //33%
    uint256 public constant privateCliff = 0 days;
    uint256 public constant publicCliff = 0 days;
    uint256 public constant liqCliff = 30 days;
    uint256 public constant lpwRewardsCliff = 30 days;
    uint256 public constant lpgrantsCliff = 60 days;
    uint256 public constant ecoCliff = 120 days;
    uint256 public constant trademiningCliff = 10 days;
    uint256 public constant teamCliff = 180 days;
    uint256 public constant advisoryCliff = 60 days;
    uint256 public constant treasuryCliff = 30 days;

    //durations
    uint256 public constant seedPeriods = 6;
    uint256 public constant privatePeriods = 6;
    uint256 public constant publicPeriods = 3;
    uint256 public constant liqPeriods = 2;
    uint256 public constant lprewardsPeriods = 3;
    uint256 public constant lpgrantsPeriods = 3;
    uint256 public constant ecoPeriods = 6;
    uint256 public constant trademiningPeriods = 3;
    uint256 public constant teamPeriods = 12;
    uint256 public constant advisorsPeriods = 12;
    uint256 public constant treasuryPeriods = 1;
}
