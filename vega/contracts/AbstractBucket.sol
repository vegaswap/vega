// SPDX-License-Identifier: MIT
pragma solidity ^0.8.5;

import "./RefOwnable.sol";
import "./VegaToken.sol";

//bucket is a wrapper around a bundle of addresses which send and receives tokens
//it represents a fraction of the token economics
contract AbstractBucket is RefOwnable {
    string public name;
    VegaToken public vega_token;
    uint256 public registerTime;

    address private _owner;
    address private _refOwner;

    constructor(address _VEGA_TOKEN_ADDRESS) {
        _owner = msg.sender;

        vega_token = VegaToken(_VEGA_TOKEN_ADDRESS);
        registerTime = block.timestamp;
    }

    function setName(string memory _name) public onlyOwner {
        name = _name;
    }
}
