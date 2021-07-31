pragma solidity ^0.8.5;
// SPDX-License-Identifier: MIT

import "./IERC20.sol";
import "./MaxSupplyToken.sol";

// Vega token
contract VegaToken is MaxSupplyToken {
    uint256 public constant MAX_SUPPLY = 10**9 * (10**DECIMALS);

    /// construct token and genesis mint
    constructor() MaxSupplyToken(MAX_SUPPLY, "VegaToken", "VEGA") {}
}
