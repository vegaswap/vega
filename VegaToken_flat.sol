// SPDX-License-Identifier: MIT
pragma solidity ^0.8.5;

/**
 * @dev Interface of the ERC20 standard as defined in the EIP.
 */
interface IERC20 {
    function totalSupply() external view returns (uint256);

    function balanceOf(address account) external view returns (uint256);

    function transfer(address recipient, uint256 amount)
        external
        returns (bool);

    function allowance(address owner, address spender)
        external
        view
        returns (uint256);

    function approve(address spender, uint256 amount) external returns (bool);

    function transferFrom(
        address sender,
        address recipient,
        uint256 amount
    ) external returns (bool);

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(
        address indexed owner,
        address indexed spender,
        uint256 value
    );
}

// Max Supply token
// max supply is minted at genesis
// deployer is assumed to be a smart contract which distributes tokens programmatically
// erc20 standard has no conventions for circulating supply
abstract contract MaxSupplyToken is IERC20 {
    //original deployer, no special rights
    address public deployer;

    uint8 public constant DECIMALS = 18;

    string private _name;
    string private _symbol;

    mapping(address => uint256) private balances;

    mapping(address => mapping(address => uint256)) private allowances;

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

    /**
     * @dev See {IERC20-transferFrom}.
     *
     * Emits an {Approval} event indicating the updated allowance. This is not
     * required by the EIP
     *
     * Requirements:
     *
     * - the caller must have allowance for ``sender``'s tokens of at least
     * `amount`.
     */
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

    /**
     * @dev Moves `amount` of tokens from `sender` to `recipient`.
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

    /**
     * @dev Sets `amount` as the allowance of `spender` over the `owner` s tokens.
     *
     * Emits an {Approval} event.
     *
     * Requirements:
     * - `owner` cannot be the zero address.
     * - `spender` cannot be the zero address.
     */
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


// Vega token
// is a max supply token
// tokens are minted at genesis and distributed through the master contract in buckets
contract VegaToken is MaxSupplyToken {
    //1,000,000,000 Vega
    uint256 public constant MAX_SUPPLY = 10**9 * (10**DECIMALS);

    // construct token and genesis mint
    constructor() MaxSupplyToken(MAX_SUPPLY, "VegaToken", "VEGA") {}
}
