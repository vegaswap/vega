// SPDX-License-Identifier: MIT
pragma solidity ^0.8.5;

// multi-ownable contract
// current owners can add new owner
abstract contract MultiOwnable {
    address[] private _owners;

    /**
     * @dev Initializes the contract setting the deployer as the initial owner
     */
    constructor() {
        _owners.push(msg.sender);
    }

    // a current owner adds a new owner
    function addNewOwner(address f) public onlyMultiOwners {
        _owners.push(f);
    }

    /**
     * @dev Returns the address of the current owners
     */
    function owners() public view virtual returns (address[] memory) {
        return _owners;
    }

    function inOwnerlist(address f) public view returns (bool) {
        for (uint256 i = 0; i < _owners.length; i++) {
            if (_owners[i] == f) {
                return true;
            }
        }
        return false;
    }

    /**
     * @dev Throws if called by any account other than the owners
     */
    modifier onlyMultiOwners() {
        require(inOwnerlist(msg.sender), "Ownable: caller is not one of the owners");
        _;
    }
}
