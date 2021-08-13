// SPDX-License-Identifier: MIT
pragma solidity ^0.8.5;

// Non transferrable Tokens (NRT)
import "./Ownable.sol";
import "./Util.sol";

contract NRT is Ownable {
    //issue date

    uint256 public issuedSupply;
    uint256 public outstandingSupply;
    uint256 public redeemedSupply;
    uint8 public constant decimals = 18;
    string public symbol;

    mapping(address => uint256) private _balances;

    event Issued(address account, uint256 amount);
    event Redeemed(address account, uint256 amount);

    constructor(string memory _symbol) {
        symbol = _symbol;
    }

    {{ debugfunctions }}

    // Creates amount of NRT and assigns them to account
    function issue(address account, uint256 amount) public onlyOwner {
        require(account != address(0), errorMessage("can't issue to zero address"));

        _balances[account] += amount;
        outstandingSupply += amount;
        issuedSupply += amount;

        emit Issued(account, amount);
    }

    // redeems amount of NRT and reduces them from account
    function redeem(address account, uint256 amount) public onlyOwner {
        require(account != address(0), errorMessage("can't redeeem to zero address"));
        require(_balances[account] >= amount, errorMessage("Insufficent balance"));

        _balances[account] -= amount;
        outstandingSupply -= amount;
        redeemedSupply += amount;

        emit Redeemed(account, amount);
    }

    function balanceOf(address account) public view returns (uint256) {
        return _balances[account];
    }
}
