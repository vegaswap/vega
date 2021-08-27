# @version ^0.2.14

name: String[15]
# VegaToken: public vega_token
registerTime: uint256
# string[100]
days: constant(uint256) = 86400
DEFAULT_PERIOD: constant(uint256) = 30 * days
cliffTime: uint256
endTime: uint256
totalAmount: uint256
numPeriods: uint256
initialized: bool
totalWithdrawnAmount: uint256
totalClaimAmount: uint256
owner: address

# Events
# event TokenExchange:
#     buyer: indexed(address)


@external
def __init__(
    _name: String[15],
    _VEGA_TOKEN_ADDRESS: address,
    _cliffTime: uint256,
    _numPeriods: uint256,
    _totalAmount: uint256,
):
    assert _VEGA_TOKEN_ADDRESS != ZERO_ADDRESS, "Vegatoken is zero address"
    assert _cliffTime >= block.timestamp, "VESTINGBUCKET: cliff must be in the future"
    assert _numPeriods > 0, "numPeriods must be larger than 0"
    assert _numPeriods < 25, "numPeriods must be smaller than 25"
    self.name = _name
    # vega_token = VegaToken(_VEGA_TOKEN_ADDRESS)
    self.registerTime = block.timestamp
    self.cliffTime = _cliffTime
    self.numPeriods = _numPeriods
    self.totalAmount = _totalAmount
    self.totalWithdrawnAmount = 0
    self.totalClaimAmount = 0
    self.initialized = False
    self.owner = msg.sender

    # self.endTime = self.getEndTime(bucketAmountPerPeriod)


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
    duration: uint256 = DEFAULT_PERIOD * (
        self.ceildiv(self.totalAmount, bucketAmountPerPeriod)
    )
    self.endTime = self.cliffTime + duration
    assert duration < 731 * days, "VESTINGBUCKET: don't vest more than 2 years"
    self.initialized = True


@internal
def linearFrom(
    _amountPerPeriod: uint256,
    _totalAmount: uint256,
) -> uint256:
    return DEFAULT_PERIOD * (self.ceildiv(self.totalAmount, _amountPerPeriod))


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
    # // at cliff, one amount is withdrawable
    validPeriodCount: uint256 = timeSinceCliff / DEFAULT_PERIOD + 1
    potentialReturned: uint256 = validPeriodCount * amountPerPeriod

    if potentialReturned > self.totalAmount:
        return self.totalAmount

    return potentialReturned


@external
def getVestedAmountPeriod(
    amountPerPeriod: uint256,
) -> uint256:
    return self.getVestedAmountPeriodI(amountPerPeriod)


@external
def depositOwner(amount: uint256):
    assert msg.sender == self.owner, "not the owner"
    
    # require(vega_token.allowance(msg.sender, address(this)) >= amount, "not enough allowance");
    # bool transferSuccess = vega_token.transferFrom(
    #         msg.sender,
    #         address(this),
    #         amount
    #     );
    #     require(transferSuccess, "VESTINGBUCKET: deposit failed");
    #     emit DepositOwner(msg.sender, amount);


# def addClaim(address _claimAddress, uint256 _claimTotalAmount)
# def getVestedAmount(Claim memory claim) public view returns (uint256) :
# def getVestableAmount(address _claimAddress)
# def vestClaimMax(address _claimAddress) public :
# def allClaim() public onlyRefOwner :
# def withdrawOwner(uint256 amount) public onlyRefOwner :
# def revokeClaim(address _claimAddress) public onlyRefOwner :

# struct Claim
# mapping(address => Claim) public claims;
# address[] public claimAddresses;
# uint256 public totalClaimAmount;
# uint256 public totalWithdrawnAmount;
