#!/usr/bin/python3
import brownie

from brownie import chain, VegaToken, VestingBucket, accounts
import time

days = 60*60*24
days30 = days*30


def test_timetravel_basic(accounts, vestingmath, token):
    current = chain.time()
    zz = 100000
    chain.sleep(zz)
    current2 = chain.time()
    assert current2 - current == zz

    vbucket = VestingBucket.deploy(
        token, current2+100, 1, 100, {'from': accounts[0]})
    assert vbucket.getCurrentTime() == current2

    #assert vbucket.endTime() == 0    

    #end = vestingbucket.endTime()


def test_timetravel(accounts, vestingmath, token):

    current = chain.time()
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
    

    assert calc_endtime > current 

    assert amountPerPeriod == 100

    vestingbucket = VestingBucket.deploy(
        token, cliff, numperiods, total, {'from': accounts[0]})
    assert vestingbucket.totalAmount() == total

    untilend = vestingbucket.endTime() - current
    assert untilend == 20 * DFP    
    chain.mine(timestamp=untilend)


def test_claimend(accounts, vestingmath, token):
    # test vest at end of the time
    DFP = vestingmath.DEFAULT_PERIOD()
    cliff = int(time.time()) + 1 * DFP
    numperiods = 10
    total = 1000
    vestingbucket = VestingBucket.deploy(
        token, cliff, numperiods, total, {'from': accounts[0]})
    
    chain.sleep(DFP*2+1)
    ct = vestingbucket.getCurrentTime()
    assert vestingbucket.endTime()-ct==11*DFP

def test_claimendodd(accounts, vestingmath, token):
    DFP = vestingmath.DEFAULT_PERIOD()
    cliff = int(time.time()) + 1 * DFP
    numperiods = 10
    total = 1011
    vestingbucket = VestingBucket.deploy(
        token, cliff, numperiods, total, {'from': accounts[0]})
    
    claimed = 0
    ct = vestingbucket.getCurrentTime()
    assert vestingbucket.endTime()-ct==12*DFP

def test_claimendadd(accounts, vestingmath, token):
    # test vest at end of the time
    a = accounts[0]
    a2 = accounts[1]
    DFP = vestingmath.DEFAULT_PERIOD()
    cliff = int(time.time()) + 1 * DFP
    numperiods = 10
    total = 1000
    vestingbucket = VestingBucket.deploy(
        token, cliff, numperiods, total, {'from': accounts[0]})
    
    #assert vestingbucket.endTime()-ct==11*DFP

    token.transfer(vestingbucket, 1000)
    vestingbucket.addClaim(a2, 1000,{'from': a})
    chain.mine(timestamp=cliff)

    #tt = vestingbucket.vestClaimMax(a, {'from': a})
    before = token.balanceOf(a2)
    vestingbucket.vestClaimMax(a2, {'from': a})
    after = token.balanceOf(a2)
    #assert tt > 0 
    ca = vestingbucket.claimAddresses(0)
    assert vestingbucket.totalWithdrawnAmount() == 100
    assert vestingbucket.claims(ca)['claimAddress'] == ca
    assert vestingbucket.claims(ca)['claimAddress'] == a2
    assert vestingbucket.claims(ca)['withdrawnAmount'] == 100
    assert after-before == 100

    for n in range(1,10):
        chain.mine(timestamp=cliff+DFP*n)
        before = token.balanceOf(a2)
        vestingbucket.vestClaimMax(a2, {'from': a})
        after = token.balanceOf(a2)
        assert vestingbucket.totalWithdrawnAmount() == 100*n
        assert after-before == 100

    after = token.balanceOf(a2)
    assert after == 1000
    
    assert token.balanceOf(vestingbucket) == 0


def test_claimendadd(accounts, vestingmath, token):
    # test vest at end of the time
    a = accounts[0]
    a2 = accounts[1]
    DFP = vestingmath.DEFAULT_PERIOD()
    cliff = int(time.time()) + 1 * DFP
    numperiods = 10
    total = 1050
    vestingbucket = VestingBucket.deploy(
        token, cliff, numperiods, total, {'from': accounts[0]})
    
    token.transfer(vestingbucket, total)
    vestingbucket.addClaim(a2, total,{'from': a})
    chain.mine(timestamp=cliff)

    before = token.balanceOf(a2)
    vestingbucket.vestClaimMax(a2, {'from': a})
    after = token.balanceOf(a2)
    ca = vestingbucket.claimAddresses(0)
    assert vestingbucket.totalWithdrawnAmount() == 105
    assert vestingbucket.claims(ca)['claimAddress'] == ca
    assert vestingbucket.claims(ca)['claimAddress'] == a2
    assert vestingbucket.claims(ca)['withdrawnAmount'] == 105
    assert after-before == 105

    for n in range(1,9):
        chain.mine(timestamp=cliff+DFP*n)
        before = token.balanceOf(a2)
        vestingbucket.vestClaimMax(a2, {'from': a})
        after = token.balanceOf(a2)
        assert after-before == 105

    #assert token.balanceOf(vestingbucket) == 33

    chain.mine(timestamp=cliff+DFP*11)
    before = token.balanceOf(a2)
    vestingbucket.vestClaimMax(a2, {'from': a})
    after = token.balanceOf(a2)
    assert after-before == 105

    assert after == 1050
    
    assert token.balanceOf(vestingbucket) == 0




    #x = vestingbucket.getVestableAmountAll()
    #assert x == 100

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
