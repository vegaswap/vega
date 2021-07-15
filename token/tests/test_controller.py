# #!/usr/bin/python3
# import brownie

# from brownie import chain, VegaToken, accounts
# import time

# days = 60*60*24
# days30 =  days*30

# def test_vega(accounts, token, controller):
#     a = accounts[0]

#     dec = token.decimals()
#     assert dec == 18


#     assert controller.DEFAULT_PERIOD() == days30

#     #t1 = int(time.time() + 5 * days)
#     #assert controller.getEndTime(t1, 10, 100) == t1 * 10 * days30
#     assert controller.getEndTime(0, 10, 100) == 10 * days30

#     t1 = int(time.time())
#     assert controller.getEndTime(t1, 10, 100) == t1 + 10 * days30

#     #// invalid registerTime, cliffTime should throw error
#     try:
#         tx = controller.registerVestingSchedule(a,  int(time.time()) - 10 * days30, 10, 1000)
#     except brownie.exceptions.VirtualMachineError as e:
#         assert e.message == "VM Exception while processing transaction: revert VESTING: CLIFF_>_START"


#     cliff = int(time.time()) + 10 * days30
#     tx = controller.registerVestingSchedule(a, cliff, 10, 1000)
#     assert len(tx.events) == 1

#     #assert tx.events[0] == OrderedDict([('registeredAddress', '0x66aB6D9362d4F35596279692F0251Db635165871'), ('registerTime', 1625547693), ('endTime', 1651467693), ('cliffTime', 1677387693), ('totalAmount', 1000)])
#     assert tx.events[0]['registeredAddress'] == a
#     assert tx.events[0]['totalAmount'] == 1000

#     vs = controller.vestingSchedules(a).dict()
#     assert vs != None

#     assert vs['registeredAddress'] == a
#     assert vs['cliffTime'] == cliff
#     assert vs['endTime'] == cliff + 10 * days30
#     assert vs['terminalPeriodInMonth'] == 10
#     assert vs['amountPerPeriod'] == 100
#     assert vs['totalAmount'] == 1000
#     assert vs['withdrawnAmount'] == 0
#     assert vs['isAdded'] == True

#     #TESTCASE invalid registerTime, cliffTime should throw error

#     #// error case: duplicated address
#     try:
#         tx = controller.registerVestingSchedule(a, cliff, 10, 1000)
#         #assert tx == None
#     except brownie.exceptions.VirtualMachineError as e:
#         assert e.message == "VM Exception while processing transaction: revert VESTING: ADDRESS_ALREADY_REGISTERED"


#     #assert vs.dict() == None

# def test_vested_amount(accounts, token, controller):
#     #TODO
#     a = accounts[0]

#     dec = token.decimals()
#     assert dec == 18

#     days = 60*60*24
#     days30 =  days*30

#     # current = controller.currentTime()

#     # registerTime = current

#     # dif = 2
#     # cliffTime = registerTime + dif
#     # # cliffTime = int(time.time()) + 1 * days
#     # endTime = cliffTime
#     # amountPerTerminalPeriod = 3
#     # totalAmount = 10

#     # vested = controller.getVestedAmount(cliffTime, endTime, dif, amountPerTerminalPeriod, totalAmount)
#     # assert vested == 10

# def test_vested_amount_zero(accounts, token, controller):

#     period = 30
#     registerTime = controller.currentTime()
#     cliffTime = registerTime + 5
#     endTime = cliffTime + period

#     vested = controller.getVestedAmount(cliffTime, endTime, 2, 2, 10)
#     assert vested == 0

# def test_registertime(accounts, token, controller):
#     #it("should return correct amount with cliff time", async function () {
#     a = accounts[0]
#     t1 = chain.time()
#     assert t1 > 1625553758
#     chain.sleep(100)
#     t2 = chain.time()
#     assert t2-t1 == 100

#     cliff = int(time.time()) + 10 * days30
#     tx = controller.registerVestingSchedule(a, cliff, 10, 1000)
#     vs = controller.vestingSchedules(a).dict()
#     assert vs['registeredAddress'] == a
#     assert vs['registerTime'] == t2

# def test_amount_cliff(accounts, token, controller):
#     #it("should return correct amount with cliff time", async function () {

#     t1 = chain.time()
#     assert t1 > 1625553758
#     chain.sleep(2 * days)
#     t2 = chain.time()
#     #assert t2-t1 == 2 * days

#     zz = int(time.time())
#     #assert zz == t1

#     #assert controller.currentTime() - zz < 5

#     period = 2 * days
#     cliffTime = zz + 2 * days
#     amountPerTerminalPeriod = 3
#     totalAmount = 10
#     #   // will be auto calculated before calling getVestedAmountTest
#     #   const endTime = cliffTime.add(period * Math.ceil(totalAmount / amountPerTerminalPeriod));
#     from math import ceil
#     endTime = cliffTime + (period * ceil(totalAmount / amountPerTerminalPeriod))

#     difsleep = cliffTime - zz
#     chain.sleep(difsleep + 100)

#     print (cliffTime, endTime, period, amountPerTerminalPeriod, totalAmount)
#     #vested = controller.getVestedAmount(cliffTime, endTime, period, amountPerTerminalPeriod, totalAmount)
#     #assert vested == 3

#     # import sys
#     # import os

#     # PACKAGE_PARENT = '..'
#     # SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
#     # sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

#     # import token_util
#     # r = token_util.getVestedAmount(block_timestamp, cliffTime, endTime, period, amountPerTerminalPeriod, totalAmount)

#     # block_timestamp = chain.time()

#     #p = (1625734497, 1626425697, 172800, 3, 10)
#     r = controller.getVestedAmount(1625734497, 1626425697, 172800, 3, 10)
#     assert r == 0

#     r = controller.getVestedAmount(1625734497, 1626425697, 172800, 3, 10)
#     assert r == 0

#     blocktime = chain.time()
#     cliffTime = blocktime - 1 * days
#     endTime = blocktime + 10 * days
#     period = 1 * days
#     amountPerTerminalPeriod = 10
#     totalAmount = 100

#     timeSinceCliff = blocktime - cliffTime
#     print ("timeSinceCliff ", timeSinceCliff)

#     #r = controller.getVestedAmount(cliffTime, endTime, period, amountPerTerminalPeriod, totalAmount)
#     #assert r == 10
