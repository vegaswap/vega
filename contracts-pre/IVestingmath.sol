// SPDX-License-Identifier: MIT
pragma solidity ^0.8.5;

interface IVestingMath {

    // divide a with m and choose higher value if its round
    // a > m
    function ceildiv(uint256 a, uint256 m) external returns (uint256);
    function getEndTime(
        uint256 _cliffTime,
        uint256 _amountPerPeriod,
        uint256 _totalAmount,
        uint256 _period
    ) external returns (uint256);

    function getEndTime(
        uint256 _cliffTime,
        uint256 _amountPerPeriod,
        uint256 _totalAmount
    ) external returns (uint256);

    function getVestedAmountPeriod(
        uint256 blocktime,
        uint256 cliffTime,
        uint256 endTime,
        uint256 amountPerPeriod,
        uint256 totalAmount,
        uint256 period
    ) external returns (uint256);
       

    function getVestedAmount(
        uint256 blocktime,
        uint256 cliffTime,
        uint256 endTime,
        uint256 amountPerPeriod,
        uint256 totalAmount
    ) external returns (uint256);
}
