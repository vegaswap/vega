#!/usr/bin/python3
import brownie

from brownie import chain, VegaToken, VestingBucket, accounts
import time

days = 60*60*24
days30 = days*30


def test_basic(accounts, vestingmath, token):

    cliff = 0
    total = 10000
    period = 6
    vestingbucket = VestingBucket.deploy(
        token, cliff, period, total, {'from': accounts[0]})
    assert vestingbucket.totalAmount() == total

    a = accounts[0]

    dec = token.decimals()
    assert dec == 18

    a2 = accounts[1]
    token.transfer(vestingbucket, 10000)
    vestingbucket.addClaim(a2, 2000)

    rclaim = vestingbucket.claims(a2).dict()
    assert rclaim != None
    assert rclaim['claimAddress'] == a2
    # assert rclaim['claimTotalAmount'] == 2000

    before = token.balanceOf(vestingbucket)
    withdrawn = vestingbucket.vestClaimMax.call(a2, {'from': a2})
    assert withdrawn == 2000
    after = token.balanceOf(vestingbucket)
    dif = after - before

    # cant claim more than total
    try:
        vestingbucket.addClaim(a2, 33000)
    except Exception as e:
        assert e != None

    a3 = accounts[2]
    vestingbucket.addClaim(a3, 500)

    withdrawn = vestingbucket.vestClaimMax.call(a2, {'from': a2})
    assert withdrawn == 2000

    # assert dif == withdrawn
    # 0??
    # assert dif == -2000


def test_timetravel(accounts, vestingmath, token):

    DFP = vestingmath.DEFAULT_PERIOD()
    assert DFP == 2592000
    # ts = 100
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

    # _cliffTime +
    # (DEFAULT_PERIOD * (ceildiv(_totalAmount, _amountPerPeriod)))

    assert amountPerPeriod == 100

    vestingbucket = VestingBucket.deploy(
        token, cliff, numperiods, total, {'from': accounts[0]})
    assert vestingbucket.totalAmount() == total
    now = int(time.time())
    untilend = vestingbucket.endTime() - now
    assert untilend == 20 * DFP
    # chain.sleep(ts+10000)
    # breaks
    # chain.mine(timestamp=untilend+1)

    # assert vestingbucket.getCurrentTime() == chain.time()

    # endtime = vestingbucket.endTime()
    # assert chain.time() > endtime


def test_cliff(accounts, vestingmath, token):

    ts = 100
    cliff = int(time.time()) + ts
    total = 10000
    period = 10
    amountPerPeriod = total/period

    assert amountPerPeriod == 1000

    vestingbucket = VestingBucket.deploy(
        token, cliff, period, total, {'from': accounts[0]})
    assert vestingbucket.totalAmount() == total

    a = accounts[0]

    dec = token.decimals()
    assert dec == 18

    a2 = accounts[1]
    token.transfer(vestingbucket, 10000)
    total = 2000
    vestingbucket.addClaim(a2, total)

    ca1 = vestingbucket.claimAddresses(0)

    claim1 = vestingbucket.claims(ca1)  # ['claimAddress'])
    # ca1['claimAddress']
    claim1d = claim1.dict()

    assert claim1d['claimAddress'] == a2

    # cant withdraw while cliff
    before = token.balanceOf(vestingbucket)
    withdrawn = vestingbucket.vestClaimMax.call(a2, {'from': a2})
    assert withdrawn == 0
    after = token.balanceOf(vestingbucket)
    dif = after - before
    assert dif == 0

    now = int(time.time())
    untilend = vestingbucket.endTime() - now
    # chain.sleep(ts+10000)
    chain.sleep(untilend+1)

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


def test_addall(accounts, vestingmath, token):

    cliff = 0
    total = 1000
    period = 6
    vestingbucket = VestingBucket.deploy(
        token, cliff, period, total, {'from': accounts[0]})
    assert token.balanceOf(vestingbucket) == 0
    assert vestingbucket.totalAmount() == total

    token.transfer(vestingbucket, 2000)
    assert token.balanceOf(vestingbucket) == 2000

    tc = 0
    import random
    for i in range(1, 6):
        # r = random.randint(1, 1000)
        amount = 200
        vestingbucket.addClaim(accounts[i], amount)
        tc += amount

    total = 0
    for i in range(1, 6):
        a = accounts[i]
        vestingbucket.vestClaimMax(
            a, {'from': a})
        assert token.balanceOf(a) == 200

    assert token.balanceOf(vestingbucket) == 1000
    total_distributed = 0
    for i in range(1, 6):
        a = accounts[i]
        total_distributed += token.balanceOf(accounts[i])
    assert total_distributed == tc

    assert token.balanceOf(vestingbucket) == 1000

    # TODO test circulating is 1000
    # TODO test locked is 1000


def test_vestableall(accounts, vestingmath, token):

    ts = 0
    cliff = int(time.time()) + ts
    # cliff = ct
    total = 1000
    period = 1
    vestingbucket = VestingBucket.deploy(
        token, cliff, period, total, {'from': accounts[0]})

    assert vestingbucket.totalAmount() == total

    ct = vestingbucket.getCurrentTime()
    assert ct > 1625902477

    endtime = vestingmath.getEndTime(cliff, 500, 1000)
    print(ct, ct, endtime, 500, 1000)
    # z = vestingmath.getVestedAmountTS(ct, 0, endtime, 500, 1000)
    # z = vestingmath.getVestedAmount(0, endtime, 500, 1000)
    # assert z == 1000

    blocktime = 1625902745
    cliffTime = 1625902745
    endtime = 1631086745
    amountPerPeriod = 500
    totalAmount = 1000
    timeSinceCliff = blocktime - cliffTime
    validPeriodCount = int(timeSinceCliff / period + 1)
    potentialReturned = validPeriodCount * amountPerPeriod

    assert timeSinceCliff == 0

    # r1 = vestingmath.getVestedAmount(
    #     cliffTime, endtime, amountPerPeriod, totalAmount)

    # assert r1 == 500

    # va = vestingbucket.getVestableAmountAll()
    # assert va == 10000


def test_claimother(accounts, vestingmath, token):

    a = accounts[0]
    cliff = 0
    total = 10000
    period = 6
    vestingbucket = VestingBucket.deploy(
        token, cliff, period, total, {'from': accounts[0]})
    assert vestingbucket.totalAmount() == total

    blackhat_account = accounts[3]
    before = token.balanceOf(vestingbucket)
    reverts = False
    try:
        vestingbucket.vestClaimMax(
            a, {'from': blackhat_account})
    except:
        reverts = True

    assert reverts

    after = token.balanceOf(vestingbucket)
    assert after == before

    # a = accounts[0]
    # a2 = accounts[1]
    # token.transfer(vestingbucket, 10000)
    # with brownie.reverts("Ownable: caller is not the owner"):
    #     vestingbucket.addClaim(a2, 2000, {'from': a2})


def test_claimother(accounts, vestingmath, token):

    cliff = 0
    total = 10000
    period = 6
    vestingbucket = VestingBucket.deploy(
        token, cliff, period, total, {'from': accounts[0]})
    assert vestingbucket.totalAmount() == total

    a = accounts[0]
    a2 = accounts[1]
    token.transfer(vestingbucket, 10000)
    with brownie.reverts("Ownable: caller is not the owner"):
        vestingbucket.addClaim(a2, 2000, {'from': a2})


def test_claim_second(accounts, vestingmath, token):
    a = accounts[0]
    a2 = accounts[1]
    cliff = 0
    total = 10000
    period = 6
    vestingbucket = VestingBucket.deploy(
        token, cliff, period, total, {'from': accounts[0]})

    vestingbucket.addClaim(a2, 2000)
    with brownie.reverts("VESTINGBUCKET: claim at this address already exists"):
        vestingbucket.addClaim(a2, 2000)
