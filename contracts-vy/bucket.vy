# @version ^0.2.15

# a vesting bucket
# a bucket is a wrapper over an account with access control
# vesting occurs linearly over time
# the owner deposits funds upfront and adds claims

from vyper.interfaces import ERC20

# name of the bucket
name: String[15]
owner: address
vegaToken: address
# VegaToken: public vega_token
registerTime: uint256
# time variables
days: constant(uint256) = 86400
default_period: constant(uint256) = 30 * days
cliffTime: public(uint256)
endTime: public(uint256)
totalAmount: public(uint256)
numPeriods: public(uint256)
initialized: public(bool)
openClaimAmount: public(uint256)
totalWithdrawnAmount: public(uint256)
totalClaimAmount: public(uint256)

struct Claim:
    claimAddress: address 
    claimTotalAmount: uint256 
    amountPerPeriod: uint256 
    withdrawnAmount: uint256 
    isAdded: bool 

claims: public(HashMap[address, Claim])

event ClaimAdded:
    claimAddress: address
    claimTotalAmount: uint256
    amountPerPeriod: uint256

event DepositOwner:
    owner: address
    amount: uint256

event WithdrawOwner:
    owner: address
    amount: uint256


@external
def __init__(
    _name: String[15],
    _vegaToken: address,
    _cliffTime: uint256,
    _numPeriods: uint256,
    _totalAmount: uint256,
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

    # self.endTime = self.getEndTime(bucketAmountPerPeriod)


#div if even otherwise
@internal
def ceildiv(a: uint256, m: uint256) -> uint256:
    t: uint256 = a % m
    if t == 0:
        return a / m
    else:
        return (a + (m - t)) / m


@external
def initialize():
    bucketAmountPerPeriod: uint256 = self.totalAmount / self.numPeriods
    duration: uint256 = default_period * (
        self.ceildiv(self.totalAmount, bucketAmountPerPeriod)
    )
    self.endTime = self.cliffTime + duration
    assert duration < 731 * days, "BUCKET: don't vest more than 2 years"
    self.initialized = True


# vesting math


@internal
def linearFrom(
    _amountPerPeriod: uint256,
    _totalAmount: uint256,
) -> uint256:
    return default_period * (self.ceildiv(self.totalAmount, _amountPerPeriod))


@internal
def getEndTime(
    _amountPerPeriod: uint256,
) -> uint256:
    # return _cliffTime + (_period * (self.ceildiv(_totalAmount, _amountPerPeriod)))
    return self.cliffTime + self.linearFrom(_amountPerPeriod, self.totalAmount)


@internal
def getVestedAmountPeriodI(
    amountPerPeriod: uint256,
) -> uint256:
    if block.timestamp >= self.endTime:
        return self.totalAmount

    if block.timestamp < self.cliffTime:
        return 0

    timeSinceCliff: uint256 = block.timestamp - self.cliffTime
    # at cliff, one amount is withdrawable
    validPeriodCount: uint256 = 1 + timeSinceCliff / default_period
    potentialReturned: uint256 = validPeriodCount * amountPerPeriod

    #TOTAL?
    if potentialReturned > self.totalAmount:
        return self.totalAmount

    return potentialReturned


@external
def getVestedAmountPeriod(amountPerPeriod: uint256) -> uint256:
    return self.getVestedAmountPeriodI(amountPerPeriod)


@external
def depositOwner(amount: uint256):
    assert msg.sender == self.owner, "BUCKET: not the owner"
    assert ERC20(self.vegaToken).allowance(msg.sender, self) >= amount, "BUCKET: not enough allowance"

    assert ERC20(self.vegaToken).balanceOf(msg.sender) >= amount, "BUCKET: not enough balance"
    transferSuccess: bool = ERC20(self.vegaToken).transferFrom(msg.sender, self, amount)
    assert transferSuccess, "BUCKET: deposit failed"
    log DepositOwner(msg.sender, amount)

@external
def withdrawOwner(amount: uint256): 
    # public onlyRefOwner
    assert msg.sender == self.owner, "BUCKET: not the owner"
    bucketbalance: uint256 = ERC20(self.vegaToken).balanceOf(self)
    unclaimedbalance: uint256 = bucketbalance - self.totalClaimAmount
    assert amount <= unclaimedbalance, "BUCKET: can't withdraw claimed amounts"
    transferSuccess: bool = ERC20(self.vegaToken).transfer(msg.sender, amount)
    assert transferSuccess, "BUCKET: withdraw failed"
    log WithdrawOwner(msg.sender, amount)


@external
def addClaim(_claimAddress: address , _claimTotalAmount: uint256):
    #requires
    # if (claims[_claimAddress].isAdded)
    #         revert("VESTINGBUCKET: claim at this address already exists");

    #     require(_claimTotalAmount > 0, "VESTINGBUCKET: claim can not be zero");

    #     require(
    #         totalClaimAmount + _claimTotalAmount <= totalAmount,
    #         "VESTINGBUCKET: can not claim more than total"
    #     );

    #     uint256 bal = vega_token.balanceOf(address(this));
    #     uint256 unclaimed = bal - totalClaimAmount;
    #     require(_claimTotalAmount <= unclaimed, "VESTINGBUCKET: can not claim tokens that are not deposited");


    amountPerPeriod: uint256 = _claimTotalAmount / self.numPeriods
    existclaim: Claim = self.claims[msg.sender]
    assert existclaim == empty(Claim), "VESTINGBUCKET: claim at this address already exists"
    self.claims[msg.sender] = Claim({
        claimAddress: _claimAddress,
        amountPerPeriod: amountPerPeriod,
        claimTotalAmount: _claimTotalAmount,
        withdrawnAmount: 0,
        isAdded: True
    })
    # self.claims[msg.sender] = 1


    # claimAddresses.push(_claimAddress);
    self.totalClaimAmount += _claimTotalAmount
    self.openClaimAmount += _claimTotalAmount

    log ClaimAdded(_claimAddress, _claimTotalAmount, amountPerPeriod)

