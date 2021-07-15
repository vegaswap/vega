#!/usr/bin/python3
import brownie

from brownie import chain, VegaToken, VestingBucket, accounts
import time

days = 60*60*24
days30 = days*30


def test_timetravel(accounts, vestingmath, token):

    DFP = vestingmath.DEFAULT_PERIOD()
    assert DFP == 2592000
    cliff = int(time.time()) + 10 * DFP
    total = 1000
    period = DFP
    amountPerPeriod = 100  # total/period

    numperiods = 10

    x = vestingmath.ceildiv(total, amountPerPeriod)
    assert x == 10
    end = cliff + period * x
    assert end == cliff + DFP * 10

    calc_endtime = vestingmath.getEndTime(
        cliff, amountPerPeriod, total)
    assert calc_endtime == cliff + 10 * DFP

    assert amountPerPeriod == 100

    vestingbucket = VestingBucket.deploy(
        token, cliff, numperiods, total, {'from': accounts[0]})
    assert vestingbucket.totalAmount() == total
    now = int(time.time())
    untilend = vestingbucket.endTime() - now
    #assert untilend == 20 * DFP
    # chain.sleep(ts+10000)
    # breaks
    chain.mine(timestamp=untilend+1)
    assert vestingbucket.getCurrentTime() == chain.time()

    endtime = vestingbucket.endTime()
    assert chain.time() >= endtime

    # vestingbucket.getVestedAmount()


def test_claimend():
    # test vest at end of the time
    pass

    # endtime = vestingbucket.endTime()
    # assert chain.time() > endtime

    # calculated_total = vestingmath.getVestedAmountTS(
    #     chain.time(),
    #     cliff,
    #     endtime,
    #     amountPerPeriod,
    #     total
    # )

    # assert calculated_total == total

    # assert vestingbucket.getCurrentTime() == chain.time()

    # assert vestingbucket.getVestedAmount(
    #     claim1) == 0  # claim1d['claimTotalAmount']

    # # amountPerPeriod = total / period
    # # endtime = vestingbucket.endTime()
    # # r = vestingmath.getVestedAmount(cliff, endtime, amountPerPeriod, total)
    # # assert r == 0

    # chain.sleep(endtime - chain.time() + 1)

    # endtime = vestingbucket.endTime()
    # r = vestingmath.getVestedAmount(cliff, endtime, amountPerPeriod, total)
    # # BUG??
    # assert r == 0

    # x = vestingbucket.getVestableAmount(a2)
    # #assert x == 2000

    # z = vestingbucket.getCurrentTime()
    # chain.sleep(ts+10000)
    # #assert chain.time()
    # assert z == 0

    # before = token.balanceOf(vestingbucket)
    # withdrawn = vestingbucket.vestClaimMax.call(a2, 2000, {'from': a2})
    # assert withdrawn == 100
    # after = token.balanceOf(vestingbucket)
    # dif = after - before
    # assert dif == 1


def test_lastround(accounts, vestingmath, token):
    # test non round periods and the last withdraw
    #assert False
    pass


def test_claimall(accounts, vestingmath, token):
    # test allClaim
    #assert False
    pass
