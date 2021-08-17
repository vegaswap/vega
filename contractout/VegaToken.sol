// SPDX-License-Identifier: MIT
pragma solidity ^0.8.5;

import "./IERC20.sol";
import "./MaxSupplyToken.sol";

// Vega token
// is a max supply token
// tokens are minted at genesis and distributed through the master contract in buckets
contract VegaToken is MaxSupplyToken {
    //1,000,000,000 Vega
    uint256 public constant MAX_SUPPLY = 10**9 * (10**DECIMALS);

    // construct token and genesis mint
    constructor() MaxSupplyToken(MAX_SUPPLY, "VegaToken", "VEGA") {}
}
