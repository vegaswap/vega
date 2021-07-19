from vestingmath import getVestedAmount

cliff = 900
period = 60 * 60 * 24 * 30
endtime = cliff + 10 * period
amountPerPeriod = 13
total = 200
from vestingmath import getVestedAmount

# assert period ==

for n in range(0, 3):
    blocktime = cliff + n * period
    v = getVestedAmount(blocktime, cliff, endtime, amountPerPeriod, total, period)
    assert v == amountPerTerminalPeriod * (n + 1)

# from vestingmath import getVestedAmount

# cliff = 900
# period = 60 * 60 * 24 * 30
# endtime = cliff + 10 * period
# amountPerPeriod = 13
# total = 200

# for n in range(0, 3):
#     blocktime = cliff + n * period
#     # import pdb
#     # pdb.set_trace()
#     v = getVestedAmount(blocktime, cliff, endtime, amountPerPeriod, total, period)
#     print(v)
#     # assert v == amountPerPeriod * (n + 1)
