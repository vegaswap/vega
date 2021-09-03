days: int = 86400
default_period: int = 30 * days
import math

def ceildiv(a: int, m: int) -> int:
    return math.ceil(a / m)

class Bucket:
    def __init__(
        self, _cliffTime: int, _numPeriods: int, _totalAmount: int, _period: int
    ):
        self.cliffTime = _cliffTime
        self.numPeriods = _numPeriods
        self.totalAmount = _totalAmount
        self.period = _period
        self.totalAmount = totalAmount
        self.blocktimestamp = 0

    def validPeriod(self) -> int:
        timeSinceCliff: int = self.blocktimestamp - self.cliffTime
        # at cliff, one amount is withdrawable
        validPeriodCount: int = 1 + timeSinceCliff / self.period
        return int(validPeriodCount)



totalAmount = 1000 + 9
amountPerPeriod = 11
x = ceildiv(totalAmount, amountPerPeriod)
print(x)

_cliffTime = 0
_period = 1
_totalAmount = 100
_numPeriods = 6
b = Bucket(_cliffTime, _numPeriods, _totalAmount, _period)

# b.blocktimestamp = 10
# print(b.validPeriod())
# b.blocktimestamp = 21
# print(b.validPeriod())