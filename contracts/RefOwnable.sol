// SPDX-License-Identifier: MIT
pragma solidity ^0.8.5;

import "./Util.sol";

// RefOwnable allows for two owners
// the primary owner is the master contract
// the refowner is the owner of the master contract
abstract contract RefOwnable {
    address private _owner;
    address private _refOwner;

    /**
     * @dev Initializes the contract setting the deployer as the initial owner.
     */
    constructor() {
        _owner = msg.sender;
    }

    function setRefOwner(address _refowner) public onlyOwner {
        _refOwner = _refowner;
    }

    /**
     * @dev Returns the address of the current owner.
     */
    function owner() public view virtual returns (address) {
        return _owner;
    }

    function refOwner() public view virtual returns (address) {
        return _refOwner;
    }

    /**
     * @dev Throws if called by any account other than the owner.
     */
    modifier onlyOwner() {
        require(owner() == msg.sender, "RefOwnable: caller is not the owner");
        _;
    }

    modifier onlyRefOwner() {
        require(
            msg.sender == _refOwner || msg.sender == _owner,
            "RefOwnable: caller is not the owner or refowner"
        );
        _;
    }
}
