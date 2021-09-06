# @version ^0.2.15

# a locking bucket
# the owner deposits funds upfront and can withdraw after locktime

from vyper.interfaces import ERC20

# original deployer
owner: address
# name of the bucket
name: public(String[15])
vegaToken: address
registerTime: public(uint256)
days: constant(uint256) = 86400
unlockTime: public(uint256)
lockDuration: public(uint256)
totalAmount: public(uint256)

event DepositOwner:
    amount: uint256


event WithdrawOwner:
    amount: uint256


@external
def __init__(
    _name: String[15],
    _vegaToken: address,
    _lockDuration: uint256,
    _totalAmount: uint256
):
    assert _vegaToken != ZERO_ADDRESS, "BUCKET: Vegatoken is zero address"
    assert _unlockTime >= block.timestamp, "BUCKET: cliff must be in the future"

    self.vegaToken = _vegaToken
    self.name = _name
    self.registerTime = block.timestamp
    self.owner = msg.sender
    assert _lockDuration < 90 * days, "BUCKET: don't lock for more than 90 days"
    self.lockDuration = _lockDuration
    self.unlockTime = block.timestamp + _unlockDuration
    self.totalAmount = _totalAmount


@external
def depositOwner(amount: uint256):
    assert msg.sender == self.owner, "BUCKET: not the owner"
    assert amount == self.totalAmount, "BUCKET: wrong amount"
    assert (
        ERC20(self.vegaToken).allowance(msg.sender, self) >= amount
    ), "BUCKET: not enough allowance"

    assert (
        ERC20(self.vegaToken).balanceOf(msg.sender) >= amount
    ), "BUCKET: not enough balance"
    transferSuccess: bool = ERC20(self.vegaToken).transferFrom(msg.sender, self, amount)
    assert transferSuccess, "BUCKET: deposit failed"
    log DepositOwner(amount)

@external
def unlockMax():
    assert msg.sender == self.owner, "BUCKET: not the owner"
    assert block.timestamp > self.unlockTime, "BUCKET: not unlock time yet"
    bucketbalance: uint256 = ERC20(self.vegaToken).balanceOf(self)

    transferSuccess: bool = ERC20(self.vegaToken).transfer(self.owner, bucketbalance)

    assert transferSuccess, "BUCKET: deposit failed"

    log WithdrawOwner(bucketbalance)



