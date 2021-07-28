pragma solidity ^0.8.5;
// SPDX-License-Identifier: MIT

import "./IERC20.sol";

// Max Supply token
// max supply is minted at genesis
// erc20 standard has no convention for circulating supply, this will be handled elsewhere
// _MAX_SUPPLY: number of tokens that will ever exist (cap)
// total supply: the erc20 standard function
// no mint function, all the supply will be generated and transferred at constructor
contract MaxSupplyToken is IERC20 {
    uint8 public constant DECIMALS = 18;

    string private _name;
    string private _symbol;

    address private deployer;

    mapping(address => uint256) private balances;

    mapping(address => mapping(address => uint256)) private allowances;

    //erc20 standard
    uint256 private _totalSupply;

    /// construct token and genesis mint
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
        emit Transfer(address(0), deployer, _MAX_SUPPLY);
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

    /**
     *
     * Requirements:
     *
     * - `recipient` cannot be the zero address.
     * - the caller must have a balance of at least `amount`.
     */
    function transfer(address recipient, uint256 amount)
        public
        virtual
        override
        returns (bool)
    {
        _transfer(msg.sender, recipient, amount);
        return true;
    }

    /**
     * @dev See {IERC20-allowance}.
     */
    function allowance(address orig, address spender)
        public
        view
        virtual
        override
        returns (uint256)
    {
        return allowances[orig][spender];
    }

    /**
     * @dev See {IERC20-approve}.
     *
     * Requirements:
     *
     * - `spender` cannot be the zero address.
     */
    function approve(address orig, uint256 amount)
        public
        virtual
        override
        returns (bool)
    {
        _approve(msg.sender, orig, amount);
        return true;
    }

    /**
     * @dev See {IERC20-transferFrom}.
     *
     * Emits an {Approval} event indicating the updated allowance. This is not
     * required by the EIP. See the note at the beginning of {ERC20}.
     *
     * Requirements:
     *
     * - `sender` and `recipient` cannot be the zero address.
     * - `sender` must have a balance of at least `amount`.
     * - the caller must have allowance for ``sender``'s tokens of at least
     * `amount`.
     */
    function transferFrom(
        address sender,
        address recipient,
        uint256 amount
    ) public virtual override returns (bool) {
        _transfer(sender, recipient, amount);

        uint256 currentAllowance = allowances[sender][msg.sender];
        require(
            currentAllowance >= amount,
            "ERC20: transfer amount exceeds allowance"
        );
        //set allowance to new amount
        //OZ unchecked
        _approve(sender, msg.sender, currentAllowance - amount);

        return true;
    }

    /**
     * @dev Moves `amount` of tokens from `sender` to `recipient`.
     *
     * This internal function is equivalent to {transfer}, and can be used to
     * e.g. implement automatic token fees, slashing mechanisms, etc.
     *
     * Emits a {Transfer} event.
     *
     * Requirements:
     *
     * - `sender` cannot be the zero address.
     * - `recipient` cannot be the zero address.
     * - `sender` must have a balance of at least `amount`.
     */
    function _transfer(
        address sender,
        address recipient,
        uint256 amount
    ) internal virtual {
        require(sender != address(0), "ERC20: transfer from the zero address");
        require(recipient != address(0), "ERC20: transfer to the zero address");

        require(
            balances[sender] >= amount,
            "ERC20: transfer amount exceeds balance"
        );

        //OZ unchecked
        balances[sender] -= amount;
        balances[recipient] += amount;

        emit Transfer(sender, recipient, amount);
    }

    /**
     * @dev Sets `amount` as the allowance of `spender` over the `owner` s tokens.
     *
     * This internal function is equivalent to `approve`, and can be used to
     * e.g. set automatic allowances for certain subsystems, etc.
     *
     * Emits an {Approval} event.
     *
     * Requirements:
     * https://ethereum.stackexchange.com/questions/13523/what-is-the-zero-account-as-described-by-the-solidity-docs
     * - `owner` cannot be the zero address.
     * - `spender` cannot be the zero address.
     */
    function _approve(
        address orig,
        address spender,
        uint256 amount
    ) internal virtual {
        require(orig != address(0), "ERC20: approve from the zero address");
        require(spender != address(0), "ERC20: approve to the zero address");

        allowances[orig][spender] = amount;
        emit Approval(orig, spender, amount);
    }
}
