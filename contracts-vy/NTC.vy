# Non transferrable Tokens (NRT)
# NRTs are like certificates. they get issued and redeemed
# the issue and redeem process is uncoupled from this contract
# the owner can give other new owners the right to issue (multiowners)
# to keep track of different issuances there is a bucket id 
# to map to vesting schedule


# event Issue:
#     receiver: indexed(address)
#     amount: uint256

# event Redeem:
#     redeemer: indexed(address)
#     amount: uint256

name: public(String[64])
symbol: public(String[32])
decimals: public(uint256)
# string public bucketID;
# uint256 public redeemdate;
# uint256 public issuedSupply;
# uint256 public totalSupply;
# uint256 public redeemedSupply;

balances: public(HashMap[address, uint256])
deployer: address
count: public(uint256)
# mapping(address => uint256) private _balances
owner: address
addresses: public(address[100])
amounts: public(uint256[100])

@external
def __init__():
    # _name: String[64], _symbol: String[32], _decimals: uint256, _max_supply: uint256    
    # self.name = "NRT"
    # self.symbol = "VegaNRT"
    # self.decimals = 18
    self.count = 0
    self.owner = msg.sender

@external
def issue(addr: address, amount: uint256):
    # could check if address already there and make list unique
    assert self.balances[addr]==0
    assert msg.sender == owner
    self.balances[addr] += amount
    self.addresses[count] = addr
    self.amounts[count] = amount
    self.count += 1


@external
def redeem(addr: address, amount: uint256):
    self.balances[addr] -= amount

# @external
# def redeem():

# def balanceOf():


