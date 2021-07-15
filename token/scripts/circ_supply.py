#!/usr/bin/python3

from brownie import chain, VegaToken, VestingMath, VegaMaster, VestingBucket, accounts

import time


def show_circ(master):
    print("# buckets ", master.num_buckets())

    ta = master.vega_token()
    token = VegaToken.at(ta)

    b = VestingBucket.at(master.buckets(0))
    maxsupply = token.MAX_SUPPLY()
    total = 0
    total_vestable = 0
    for i in range(master.num_buckets()):
        b = VestingBucket.at(master.buckets(i))
        x = token.balanceOf(b)/10**18

        vestable = b.getVestableAmountAll()

        total += x
        total_vestable += vestable
        print(i, b.name(), x, vestable/10**18)

    circ = total_vestable/maxsupply
    circ_supply = total_vestable/10**18
    price = 0.012
    circ_mcap = int(price * circ_supply)
    print("total circ ", total, total_vestable, circ)
    print("circ_mcap ", circ_mcap)


def main():
    print("*** calculate initial circ supply *** ")

    a = accounts[0]
    vestingmath = VestingMath.deploy({'from': a})
    #token = VegaToken.deploy({'from': a})
    master = VegaMaster.deploy({'from': a})

    print(chain.time())

    show_circ(master)

    df = vestingmath.DEFAULT_PERIOD()
    chain.sleep(df*10)
    print(chain.time())

    show_circ(master)

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
