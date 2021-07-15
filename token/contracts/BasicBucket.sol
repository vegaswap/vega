// SPDX-License-Identifier: MIT
pragma solidity ^0.8.5;

import "./AbstractBucket.sol";
import "./VegaToken.sol";

//plain bucket without vesting
contract BasicBucket is AbstractBucket {
    constructor(address _VEGA_TOKEN_ADDRESS)
        AbstractBucket(_VEGA_TOKEN_ADDRESS)
    {}
}
