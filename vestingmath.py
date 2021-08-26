# @version ^0.2.14

days = 2592000
DEFAULT_PERIOD = 30 * days

def ceildiv(a: int, m: int) -> int:
    t: int = a % m
    if t == 0:
        return a / m
    else:
        return (a + (m - t)) / m

def linearFrom(
    _amountPerPeriod: int,
    _totalAmount: int,
    _period: int,
) -> int:
    return _period * (ceildiv(_totalAmount, _amountPerPeriod))


def getEndTimeI(
    _cliffTime: int,
    _amountPerPeriod: int,
    _totalAmount: int,
    _period: int,
) -> int:
    # return _cliffTime + (_period * (self.ceildiv(_totalAmount, _amountPerPeriod)))
    return _cliffTime + linearFrom(_amountPerPeriod, _totalAmount, _period)

def getEndTime(
    _cliffTime: int, _amountPerPeriod: int, _totalAmount: int
) -> int:
    return getEndTimeI(_cliffTime, _amountPerPeriod, _totalAmount, DEFAULT_PERIOD)


def getVestedAmountPeriodI(
    blocktime: int,
    cliffTime: int,
    endTime: int,
    amountPerPeriod: int,
    totalAmount: int,
    period: int,
) -> int:
    if blocktime >= endTime:
        return totalAmount

    if blocktime < cliffTime:
        return 0

    timeSinceCliff: int = blocktime - cliffTime
    # // at cliff, one amount is withdrawable
    validPeriodCount: int = timeSinceCliff / period + 1
    potentialReturned: int = validPeriodCount * amountPerPeriod

    if potentialReturned > totalAmount:
        return totalAmount

    return potentialReturned


def getVestedAmountPeriod(
    blocktime: int,
    cliffTime: int,
    endTime: int,
    amountPerPeriod: int,
    totalAmount: int,
) -> int:

    return getVestedAmountPeriodI(
        blocktime, cliffTime, endTime, amountPerPeriod, totalAmount, DEFAULT_PERIOD
    )
    
# def getVestedAmount(
#     blocktime, cliffTime, endTime, amountPerPeriod, totalAmount, period
# ):
#     if blocktime >= endTime:
#         return int(totalAmount)

#     # returns 0 if cliffTime is not reached
#     if blocktime < cliffTime:
#         return 0

#     timeSinceCliff = blocktime - cliffTime
#     print("timeSinceCliff ", timeSinceCliff)
#     validPeriodCount = timeSinceCliff / period + 1
#     print("validPeriodCount ", validPeriodCount)
#     # // at cliff, one amount is withdrawable
#     potentialReturned = validPeriodCount * amountPerPeriod

#     if potentialReturned > totalAmount:
#         return int(totalAmount)

#     return int(potentialReturned)