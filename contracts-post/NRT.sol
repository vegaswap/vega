// SPDX-License-Identifier: MIT
pragma solidity ^0.8.5;
// multi-ownable contract
// current owners can add new owner
abstract contract MultiOwnable {
    address[] private _owners;

    event OwnerAdded(address newowner);

    /**
     * @dev Initializes the contract setting the deployer as the initial owner
     */
    constructor() {
        _owners.push(msg.sender);
        emit OwnerAdded(msg.sender);
    }

    // a current owner adds a new owner
    function addNewOwner(address f) public onlyMultiOwners {
        _owners.push(f);
        emit OwnerAdded(msg.sender);
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
    uint256 public totalSupply;
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
        totalSupply += amount;
        issuedSupply += amount;

        emit Issue(account, amount);
    }

    // redeems amount of NRT and reduces them from account
    function redeem(address account, uint256 amount) public onlyMultiOwners {
        require(account != address(0), "zero address");
        require(_balances[account] >= amount, "Insufficent balance");
        require(block.timestamp > redeemdate, "not redeemable yet");

        _balances[account] -= amount;
        totalSupply -= amount;
        redeemedSupply += amount;

        emit Redeem(account, amount);
    }

    function balanceOf(address account) public view returns (uint256) {
        return _balances[account];
    }
}
