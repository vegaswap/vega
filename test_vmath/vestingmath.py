# @version ^0.2.14

days = 86400
default_period = 30 * days

totalAmount = 10

def ceildiv(a: int, m: int) -> int:
    t: int = a % m
    if t == 0:
        return a / m
    else:
        return (a + (m - t)) / m

def linearFrom(
    _amountPerPeriod: int,
    _totalAmount: int,
) -> int:
    return default_period * (ceildiv(_totalAmount, _amountPerPeriod))


def getEndTime(
    _cliffTime: int,
    _amountPerPeriod: int,
    _totalAmount: int,
) -> int:
    lf = linearFrom(_amountPerPeriod, _totalAmount)
    return _cliffTime + lf

def getVestedAmountPeriod(
    blocktime: int,
    cliffTime: int,
    endTime: int,
    amountPerPeriod: int,
    totalAmount: int,
) -> int:
    if blocktime >= endTime:
        return totalAmount

    if blocktime < cliffTime:
        return 0

    timeSinceCliff: int = blocktime - cliffTime
    # // at cliff, one amount is withdrawable
    validPeriodCount: int = 1+ int(timeSinceCliff / default_period)
    # print("validPeriodCount ",validPeriodCount)
    potentialReturned: int = validPeriodCount * amountPerPeriod

    if potentialReturned > totalAmount:
        return totalAmount

    return potentialReturned

