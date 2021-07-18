// SPDX-License-Identifier: MIT

pragma solidity ^0.8.5;

//ownable which allows for pas through ownership
//the primary owner is the master contract
//the refowner is the owner of the master contract
abstract contract RefOwnable {
    address private _owner;
    address private _refOwner;

    /**
     * @dev Initializes the contract setting the deployer as the initial owner.
     */
    constructor(address refowner) {
        _owner = msg.sender;
        _refOwner = refowner;
    }

    /**
     * @dev Returns the address of the current owner.
     */
    function owner() public view virtual returns (address) {
        return _owner;
    }

    /**
     * @dev Throws if called by any account other than the owner.
     */
    modifier onlyOwner() {
        require(owner() == msg.sender, "RefOwnable: caller is not the owner");
        _;
    }

    modifier onlyRefOwner() {
        //require(owner() == msg.sender, "Ownable: caller is not the owner");
        require(
            msg.sender == _refOwner || msg.sender == _owner,
            "RefOwnable: caller is not the owner of refowner"
        );
        _;
    }
}
