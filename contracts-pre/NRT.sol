// SPDX-License-Identifier: MIT
pragma solidity ^0.8.5;

import "./Ownable.sol";

// Non transferrable Tokens (NRT)
contract NRT is Ownable {

    string public symbol;
    string public name;
    string public bucketID;
    uint256 public redeemdate;
    uint256 public issuedSupply;
    uint256 public outstandingSupply;
    uint256 public redeemedSupply;
    
    uint8 public constant decimals = 18;

    mapping(address => uint256) private _balances;

    event Issued(address account, uint256 amount);
    event Redeemed(address account, uint256 amount);

    constructor(string memory _symbol, string memory _name, string memory _bucketID) {
        symbol = _symbol;
        bucketID = _bucketID;
        name = _name;
        redeemdate = block.timestamp;
    }

    function setRedeemDate(uint256 _redeemdate) public onlyOwner {
        redeemdate = _redeemdate;
    }

    // creates amount of NRT and assigns them to account
    function issue(address account, uint256 amount) public onlyOwner {
        require(account != address(0), "zero address");

        _balances[account] += amount;
        outstandingSupply += amount;
        issuedSupply += amount;

        emit Issued(account, amount);
    }

    // redeems amount of NRT and reduces them from account
    function redeem(address account, uint256 amount) public onlyOwner {
        require(account != address(0), "zero address");
        require(_balances[account] >= amount, "Insufficent balance");
        require(block.timestamp > redeemdate, "not redeemable yet");

        _balances[account] -= amount;
        outstandingSupply -= amount;
        redeemedSupply += amount;

        emit Redeemed(account, amount);
    }

    function balanceOf(address account) public view returns (uint256) {
        return _balances[account];
    }
}
