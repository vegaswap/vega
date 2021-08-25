// SPDX-License-Identifier: MIT
pragma solidity ^0.8.5;

import "./MultiOwnable.sol";

// Non transferrable Tokens (NRT)
// NRTs are like certificates. they get issued and redeemed
// the issue and redeem process is uncoupled from this contract
// the owner can give other new owners the right to issue (multiowners)
// to keep track of different issuances there is a bucket id 
// to map to vesting schedule
contract NRT is MultiOwnable {

    string public symbol;
    string public name;
    string public bucketID;
    uint256 public redeemdate;
    uint256 public issuedSupply;
    uint256 public outstandingSupply;
    uint256 public redeemedSupply;
    
    uint8 public constant decimals = 18;

    mapping(address => uint256) private _balances;

    event Issue(address account, uint256 amount);
    event Redeem(address account, uint256 amount);

    constructor(string memory _symbol, string memory _name, string memory _bucketID) {
        symbol = _symbol;
        bucketID = _bucketID;
        name = _name;
        redeemdate = block.timestamp;
    }

    function setRedeemDate(uint256 _redeemdate) public onlyMultiOwners {
        redeemdate = _redeemdate;
    }

    // creates amount of NRT and assigns them to account
    function issue(address account, uint256 amount) public onlyMultiOwners {
        require(account != address(0), "zero address");
        require(amount > 0, "issue amount should be larger than zero");

        // if (_balances[account] )
        _balances[account] += amount;
        outstandingSupply += amount;
        issuedSupply += amount;

        emit Issue(account, amount);
    }

    // redeems amount of NRT and reduces them from account
    function redeem(address account, uint256 amount) public onlyMultiOwners {
        require(account != address(0), "zero address");
        require(_balances[account] >= amount, "Insufficent balance");
        require(block.timestamp > redeemdate, "not redeemable yet");

        _balances[account] -= amount;
        outstandingSupply -= amount;
        redeemedSupply += amount;

        emit Redeem(account, amount);
    }

    function balanceOf(address account) public view returns (uint256) {
        return _balances[account];
    }
}
