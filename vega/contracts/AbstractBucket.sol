// SPDX-License-Identifier: MIT
pragma solidity ^0.8.5;

//import "./Ownable.sol";
//import "./RefOwnable.sol";
import "./VegaToken.sol";

//bucket is a wrapper around a bundle of addresses which send and receives tokens
//it represents a fraction of the token economics
contract AbstractBucket {
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

    function setRefOwner(address _refowner) public onlyOwner {
        _refOwner = _refowner;
    }

    function setName(string memory _name) public onlyOwner {
        name = _name;
    }

    function owner() public view virtual returns (address) {
        return _owner;
    }

    function refOwner() public view virtual returns (address) {
        return _refOwner;
    }

    modifier onlyOwner() {
        require(
            msg.sender == _owner,
            "AbstractBucket: caller is not the owner"
        );
        _;
    }

    modifier onlyRefOwner() {
        require(
            msg.sender == _refOwner || msg.sender == _owner,
            "AbstractBucket: caller is not the owner of refowner"
        );
        _;
    }
}
