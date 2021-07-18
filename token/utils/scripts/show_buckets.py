#!/usr/bin/python3

from brownie import VegaToken, VestingMath, VegaMaster, VestingBucket, accounts

import time


def main():
    print("*** buckets and allocation *** ")

    a = accounts[0]
    vestingmath = VestingMath.deploy({"from": a})
    # token = VegaToken.deploy({'from': a})
    master = VegaMaster.deploy({"from": a})
    print(master)
    # master = VegaMaster.at("0x602C71e4DAC47a042Ee7f46E0aee17F94A3bA0B6")

    ta = master.vega_token()
    token = VegaToken.at(ta)

    # print (master.depositAmount())

    print("# buckets ", master.bucket_num())

    total = 0
    for i in range(master.bucket_num()):
        b = VestingBucket.at(master.buckets(i))
        x = token.balanceOf(b)
        p = round(x / master.lockedSupply(), 3)
        total += x
        print(i, b.name(), x / 10 ** 18, p)

    print("\ntotal ", total)

    # l = master.lockedSupply() / 10 ** 18
    # lp = master.lockedSupply() / master.maxSupply()
    # print("lockedSupply ", l, lp)
    # rest = master.maxSupply() - master.lockedSupply()
    # rp = rest / master.maxSupply()
    # print("rest ", rest / 10 ** 18, rp)

    # b = VestingBucket.at(master.buckets(i))

    # print("lockedSupply ", token.lockedSupply()/10**18)

    # dec = master.VEGA_TOKEN.decimals()
    # print (dec)

    # dec = token.decimals()

    # b = token.balanceOf(master, {'from': a})
    # print (b)

    # a1 = token.allowance(a, master, {'from': a})
    # print (a1)

    # result = token.approve(master, 100 * 10 ** dec, {'from': a})
    # print ("result ", result)

    # a2 = token.allowance(a, master, {'from': a})
    # print (a2)

    # #time.sleep(10)

    # master.depositTokens(100 * 10 ** dec)

    # va = master.depositAmount()
    # print (va==100 * 10 ** dec)

    # b = token.balanceOf(master, {'from': a})
    # print (b)

    # # await this.vestingController.connect(owner).registerVestingSchedule(
    # #     seed.address,
    # #     (await latest()).add(this.DEFAULT_PERIOD), // after 1 month
    # #     10,
    # #     (1.25 / 100) * this.totalSupply
    # #   );

    # DEFAULT_PERIOD = 300000
    # ts = 10**9 * 10 ** dec
    # clifftime = int(time.time()) + DEFAULT_PERIOD
    # params = ("Seed", a, clifftime, 10, 0.0125*ts)
    # print (params)
    # master.registerVestingBucket("Seed", a, clifftime, 10, 1.25*ts)
    # #uint256 endTime = getEndTime(_cliffTime, amountPerPeriod, _totalAmount);

    # #l = master.vestingBuckets()[a]
    # #l = master.getBucket(a)
    # #print (type(l))
    # #.length
    # #print (l.name)
    # print (master.buckets_registered())

    # end = master.getEndTime(clifftime, 100, 1000)
    # print (end)

    # b = master.getBucket(a)
    # master.getVestedAmount(b, 100)
