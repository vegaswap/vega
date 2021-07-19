def getVestedAmount(
    blocktime, cliffTime, endTime, amountPerPeriod, totalAmount, period
):
    if blocktime >= endTime:
        return int(totalAmount)

    # returns 0 if cliffTime is not reached
    if blocktime < cliffTime:
        return 0

    timeSinceCliff = blocktime - cliffTime
    validPeriodCount = timeSinceCliff / period + 1
    # // at cliff, one amount is withdrawable
    potentialReturned = validPeriodCount * amountPerPeriod

    if potentialReturned > totalAmount:
        return int(totalAmount)

    return int(potentialReturned)
