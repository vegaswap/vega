// SPDX-License-Identifier: MIT
pragma solidity ^0.8.5;

import "./IERC20.sol";

// Max Supply token
// max supply is minted at genesis
// erc20 standard has no conventions for circulating supply
abstract contract MaxSupplyToken is IERC20 {
    //original deployer, no special rights
    address public deployer;
    //18 decimals by default
    uint8 public constant DECIMALS = 18;
    //name of the token
    string private _name;
    //symbol of the token. it is not enforceable and registered offchain
    string private _symbol;
    //map of balances
    mapping(address => uint256) private balances;
    //map of allownce to other contracts
    mapping(address => mapping(address => uint256)) private allowances;
    //total supply which is max supply
    uint256 private _totalSupply;

    // construct token and genesis mint
    constructor(
        uint256 _MAX_SUPPLY,
        string memory __name,
        string memory __symbol
    ) {
        deployer = msg.sender;
        _name = __name;
        _symbol = __symbol;
        // create the max supply once, all other calls are transfers
        _totalSupply = _MAX_SUPPLY;
        balances[deployer] = _MAX_SUPPLY;
    }

    function name() public view virtual returns (string memory) {
        return _name;
    }

    function symbol() public view virtual returns (string memory) {
        return _symbol;
    }

    function decimals() public view virtual returns (uint8) {
        return DECIMALS;
    }

    function totalSupply() public view virtual override returns (uint256) {
        return _totalSupply;
    }

    function balanceOf(address account)
        public
        view
        virtual
        override
        returns (uint256)
    {
        return balances[account];
    }

    function transfer(address recipient, uint256 amount)
        public
        virtual
        override
        returns (bool)
    {
        _transfer(msg.sender, recipient, amount);
        return true;
    }

    function allowance(address orig, address spender)
        public
        view
        virtual
        override
        returns (uint256)
    {
        return allowances[orig][spender];
    }

    function approve(address orig, uint256 amount)
        public
        virtual
        override
        returns (bool)
    {
        _approve(msg.sender, orig, amount);
        return true;
    }

    function transferFrom(
        address sender,
        address recipient,
        uint256 amount
    ) public virtual override returns (bool) {        

        uint256 currentAllowance = allowances[sender][msg.sender];
        require(
            currentAllowance >= amount,
            "MaxSupplyToken: transfer amount exceeds allowance"
        );

        _transfer(sender, recipient, amount);

        //set allowance to new amount
        _approve(sender, msg.sender, currentAllowance - amount);

        return true;
    }

    function _transfer(
        address sender,
        address recipient,
        uint256 amount
    ) internal virtual {
        require(sender != address(0), "MaxSupplyToken: transfer from the zero address");
        require(recipient != address(0), "MaxSupplyToken: transfer to the zero address");

        require(
            balances[sender] >= amount,
            "MaxSupplyToken: transfer amount exceeds balance"
        );

        balances[sender] -= amount;
        balances[recipient] += amount;

        emit Transfer(sender, recipient, amount);
    }

    function _approve(
        address orig,
        address spender,
        uint256 amount
    ) internal virtual {
        require(orig != address(0), "MaxSupplyToken: approve from the zero address");
        require(spender != address(0), "MaxSupplyToken: approve to the zero address");

        allowances[orig][spender] = amount;
        emit Approval(orig, spender, amount);
    }
}