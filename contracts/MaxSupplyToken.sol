// SPDX-License-Identifier: MIT
pragma solidity ^0.8.5;

import "./IERC20.sol";
import "./Util.sol";

// Max Supply token

// max supply is minted at genesis
// deployer is assumed to be a smart contract which distributes tokens programmatically
// erc20 standard has no conventions for circulating supply
// adapted from OZ
abstract contract MaxSupplyToken is IERC20 {
    //original deployer, no special rights
    address private deployer;

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

    {{ debugfunctions }}

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
     * required by the EIP. See the note at the beginning of {ERC20}.
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
        //OZ does transfer here even though check for allowance comes later
        _transfer(sender, recipient, amount);

        uint256 currentAllowance = allowances[sender][msg.sender];
        require(
            currentAllowance >= amount,
            errorMessage("transfer amount exceeds allowance")
        );
        //set allowance to new amount
        //Openzeppelin has unchecked here
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
        require(
            sender != address(0),
            errorMessage("transfer from the zero address")
        );
        require(
            recipient != address(0),
            errorMessage("transfer to the zero address")
        );

        require(
            balances[sender] >= amount,
            errorMessage("transfer amount exceeds balance")
        );

        //Openzeppelin has unchecked here
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
     * - `owner` cannot be the zero address.
     * - `spender` cannot be the zero address.
     */
    function _approve(
        address orig,
        address spender,
        uint256 amount
    ) internal virtual {
        require(
            orig != address(0),
            errorMessage("approve from the zero address")
        );
        require(
            spender != address(0),
            errorMessage("approve to the zero address")
        );

        allowances[orig][spender] = amount;
        emit Approval(orig, spender, amount);
    }
}
