# @version ^0.2.14

days: constant(uint256) = 2592000
DEFAULT_PERIOD: constant(uint256) = 30 * days

@internal
def ceildiv(a: uint256, m: uint256) -> uint256:
    t: uint256 = a % m
    if t == 0:
        return a / m
    else:
        return (a + (m - t)) / m

@internal
def linearFrom(
    _amountPerPeriod: uint256,
    _totalAmount: uint256,
    _period: uint256,
) -> uint256:
    return _period * (self.ceildiv(_totalAmount, _amountPerPeriod))


@internal
def getEndTimeI(
    _cliffTime: uint256,
    _amountPerPeriod: uint256,
    _totalAmount: uint256,
    _period: uint256,
) -> uint256:
    # return _cliffTime + (_period * (self.ceildiv(_totalAmount, _amountPerPeriod)))
    return _cliffTime + self.linearFrom(_amountPerPeriod, _totalAmount, _period)

@external
def getEndTime(
    _cliffTime: uint256, _amountPerPeriod: uint256, _totalAmount: uint256
) -> uint256:
    return self.getEndTimeI(_cliffTime, _amountPerPeriod, _totalAmount, DEFAULT_PERIOD)


@internal
def getVestedAmountPeriodI(
    blocktime: uint256,
    cliffTime: uint256,
    endTime: uint256,
    amountPerPeriod: uint256,
    totalAmount: uint256,
    period: uint256,
) -> uint256:
    if blocktime >= endTime:
        return totalAmount

    if blocktime < cliffTime:
        return 0

    timeSinceCliff: uint256 = blocktime - cliffTime
    # // at cliff, one amount is withdrawable
    validPeriodCount: uint256 = timeSinceCliff / period + 1
    potentialReturned: uint256 = validPeriodCount * amountPerPeriod

    if potentialReturned > totalAmount:
        return totalAmount

    return potentialReturned


@external
def getVestedAmountPeriod(
    blocktime: uint256,
    cliffTime: uint256,
    endTime: uint256,
    amountPerPeriod: uint256,
    totalAmount: uint256,
) -> uint256:

    return self.getVestedAmountPeriodI(
        blocktime, cliffTime, endTime, amountPerPeriod, totalAmount, DEFAULT_PERIOD
    )