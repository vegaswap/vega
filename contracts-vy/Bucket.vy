# @version ^0.2.15

# a vesting bucket
# a bucket is a wrapper over an account with access control
# vesting occurs linearly over time
# the owner deposits funds upfront and adds claims

from vyper.interfaces import ERC20


interface ClaimList:
    def addresses(i: uint256) -> address:
        nonpayable

    def amounts(i: uint256) -> uint256:
        nonpayable

    def count() -> uint256:
        nonpayable


# original deployer
owner: address
# name of the bucket
name: public(String[15])
vegaToken: address
registerTime: public(uint256)
days: constant(uint256) = 86400
default_period: constant(uint256) = 30 * days
period: public(uint256)
cliffTime: public(uint256)
duration: public(uint256)
endTime: public(uint256)
totalAmount: public(uint256)
numPeriods: public(uint256)
initialized: public(bool)
openClaimAmount: public(uint256)
totalWithdrawnAmount: public(uint256)
totalClaimAmount: public(uint256)
claim_addresses: public(address[1000])
claimCount: public(uint256)

struct Claim:
    claimAddress: address
    claimTotalAmount: uint256
    amountPeriod: uint256
    withdrawnAmount: uint256
    isAdded: bool


claims: public(HashMap[address, Claim])


event DepositOwner:
    owner: address
    amount: uint256


event WithdrawOwner:
    owner: address
    amount: uint256


event ClaimAdded:
    claimAddress: address
    claimTotalAmount: uint256


event WithdrawClaim:
    claimAddress: address
    amount: uint256


@external
def __init__(
    _name: String[15],
    _vegaToken: address,
    _cliffTime: uint256,
    _numPeriods: uint256,
    _totalAmount: uint256,
    _period: uint256,
):
    assert _vegaToken != ZERO_ADDRESS, "BUCKET: Vegatoken is zero address"
    assert _cliffTime >= block.timestamp, "BUCKET: cliff must be in the future"
    assert _numPeriods > 0, "BUCKET: numPeriods must be larger than 0"
    assert _numPeriods < 25, "BUCKET: numPeriods must be smaller than 25"
    self.vegaToken = _vegaToken
    self.name = _name
    self.registerTime = block.timestamp
    self.cliffTime = _cliffTime
    self.numPeriods = _numPeriods
    self.totalAmount = _totalAmount
    self.totalWithdrawnAmount = 0
    self.totalClaimAmount = 0
    self.initialized = False
    self.owner = msg.sender
    self.period = _period
    self.claimCount = 0


# div if even otherwise ceil
@internal
def ceildiv(a: uint256, m: uint256) -> uint256:
    t: uint256 = a % m
    if t == 0:
        return a / m
    else:
        return (a + (m - t)) / m


@external
def initialize():
    assert msg.sender == self.owner, "BUCKET: not the owner"
    assert not self.initialized
    amountPerPeriod: uint256 = self.totalAmount / self.numPeriods
    self.duration = self.period * self.ceildiv(self.totalAmount, amountPerPeriod)
    assert self.duration < 731 * days, "BUCKET: don't vest more than 2 years"
    self.endTime = self.cliffTime + self.duration
    self.initialized = True


@internal
def currentPeriod() -> uint256:
    timeSinceCliff: uint256 = block.timestamp - self.cliffTime
    # at cliff, one amount is withdrawable
    validPeriodCount: uint256 = 1 + timeSinceCliff / default_period
    return validPeriodCount


@external
def depositOwner(amount: uint256):
    assert msg.sender == self.owner, "BUCKET: not the owner"
    assert (
        ERC20(self.vegaToken).allowance(msg.sender, self) >= amount
    ), "BUCKET: not enough allowance"

    assert (
        ERC20(self.vegaToken).balanceOf(msg.sender) >= amount
    ), "BUCKET: not enough balance"
    transferSuccess: bool = ERC20(self.vegaToken).transferFrom(msg.sender, self, amount)
    assert transferSuccess, "BUCKET: deposit failed"
    log DepositOwner(msg.sender, amount)


@external
def withdrawOwner(amount: uint256):
    assert msg.sender == self.owner, "BUCKET: not the owner"
    bucketbalance: uint256 = ERC20(self.vegaToken).balanceOf(self)
    unclaimedbalance: uint256 = bucketbalance - self.openClaimAmount
    assert amount <= unclaimedbalance, "BUCKET: can't withdraw claimed amounts"
    transferSuccess: bool = ERC20(self.vegaToken).transfer(msg.sender, amount)
    assert transferSuccess, "BUCKET: withdraw failed"
    log WithdrawOwner(msg.sender, amount)


@internal
def _getVestableAmount(_claimAddress: address) -> uint256:
    claim: Claim = self.claims[_claimAddress]

    if block.timestamp < self.cliffTime:
        return 0

    if block.timestamp >= self.endTime:
        return claim.claimTotalAmount

    return self.currentPeriod() * claim.amountPeriod


@external
def getVestableAmount(_claimAddress: address) -> uint256:
    return self._getVestableAmount(_claimAddress)


@internal
def capat(amount: uint256, cap: uint256) -> uint256:
    if amount > cap:
        return cap
    else:
        return amount

@internal
def _vestClaimMax(_claimAddress: address):
    assert self.claims[_claimAddress].isAdded, "BUCKET: claim does not exist"

    claim: Claim = self.claims[_claimAddress]

    vestableAmount: uint256 = self._getVestableAmount(_claimAddress)
    vestableAmount = self.capat(vestableAmount, claim.claimTotalAmount)

    withdrawAmount: uint256 = vestableAmount - claim.withdrawnAmount
    totalAfterwithdraw: uint256 = claim.withdrawnAmount + withdrawAmount

    assert (
        totalAfterwithdraw <= claim.claimTotalAmount
    ), "BUCKET: can not withdraw more than total"

    assert withdrawAmount > 0, "BUCKET: no amount claimed"

    assert ERC20(self.vegaToken).transfer(
        _claimAddress, withdrawAmount
    ), "BUCKET: transfer failed"

    log WithdrawClaim(claim.claimAddress, withdrawAmount)

    claim.withdrawnAmount += withdrawAmount
    self.totalWithdrawnAmount += withdrawAmount
    self.openClaimAmount -= withdrawAmount

@external
def vestClaimMax(_claimAddress: address):
    isclaimer: bool = msg.sender == _claimAddress
    assert msg.sender == self.owner or isclaimer, "BUCKET: not the owner or claimer"

    self._vestClaimMax(_claimAddress)


@internal
def _addClaim(_claimAddress: address, _claimTotalAmount: uint256):
    assert not self.claims[_claimAddress].isAdded, "BUCKET: added already"

    assert _claimTotalAmount > 0, "BUCKET: claim can not be zero"

    assert (
        self.totalClaimAmount + _claimTotalAmount <= self.totalAmount
    ), "BUCKET: can not claim more than total"

    bal: uint256 = ERC20(self.vegaToken).balanceOf(self)
    unclaimed: uint256 = bal - self.totalClaimAmount
    assert (
        _claimTotalAmount <= unclaimed
    ), "BUCKET: can not claim tokens that are not deposited"

    _amountPeriod: uint256 = _claimTotalAmount / self.numPeriods
    existclaim: Claim = self.claims[_claimAddress]
    assert existclaim == empty(Claim), "BUCKET: claim at this address already exists"
    self.claims[_claimAddress] = Claim(
        {
            claimAddress: _claimAddress,
            amountPeriod: _amountPeriod,
            claimTotalAmount: _claimTotalAmount,
            withdrawnAmount: 0,
            isAdded: True,
        }
    )

    self.claimCount += 1
    self.claim_addresses[self.claimCount] = _claimAddress

    self.totalClaimAmount += _claimTotalAmount
    self.openClaimAmount += _claimTotalAmount

    log ClaimAdded(_claimAddress, _claimTotalAmount)


@external
def addClaim(_claimAddress: address, _claimTotalAmount: uint256):
    assert msg.sender == self.owner, "BUCKET: not owner"
    self._addClaim(_claimAddress, _claimTotalAmount)


@external
def vestAll():
    assert msg.sender == self.owner, "BUCKET: not owner"
    for i in range(0, 1000):
        addr: address = self.claim_addresses[i]
        if self.claims[addr].isAdded:
            self._vestClaimMax(addr)
        else:
            return


@external
def addClaimsBatch(list_addr: address):
    for i in range(0, 1000):
        amount: uint256 = ClaimList(list_addr).amounts(i)
        if amount > 0:
            self._addClaim(ClaimList(list_addr).addresses(i), amount)
        else:
            return
