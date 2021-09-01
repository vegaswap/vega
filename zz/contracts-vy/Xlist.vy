# a simple arraylist of address and amounts

name: public(String[64])
symbol: public(String[32])
decimals: public(uint256)
issuedSupply: public(uint256)

# string public bucketID;

deployer: address
count: public(uint256)
owner: address
addresses: public(address[100])
amounts: public(uint256[100])


@external
def __init__():
    self.count = 0
    self.owner = msg.sender


@external
def addItem(addr: address, amount: uint256):
    assert msg.sender == self.owner
    self.addresses[self.count] = addr
    self.amounts[self.count] = amount
    self.count += 1


@external
def getAddress(i: uint256) -> address:
    return self.addresses[i]


@external
def getAmount(i: uint256) -> uint256:
    return self.amounts[i]
