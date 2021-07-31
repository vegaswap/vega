#!/usr/bin/python3
import brownie

from brownie import chain, VegaToken, VestingBucket, accounts
import time

days = 60 * 60 * 24
days30 = days * 30


def test_timetravel_basic(accounts, vestingmath, token):
    current = chain.time()
    zz = 100000
    chain.sleep(zz)
    current2 = chain.time()
    assert current2 - current == zz

    vbucket = VestingBucket.deploy(token, current2 + 100, 1, 100, {"from": accounts[0]})
    # assert chain.time() == current2

    # assert vbucket.endTime() == 0

    # end = vestingbucket.endTime()


def test_timetravel(accounts, vestingmath, token):

    current = chain.time()
    DFP = vestingmath.DEFAULT_PERIOD()
    assert DFP == 2592000
    cliff = chain.time() + 10 * DFP
    total = 1000
    period = DFP
    amountPerPeriod = 100  # total/period

    numperiods = 10

    x = vestingmath.ceildiv(total, amountPerPeriod)
    assert x == 10
    end = cliff + period * x
    assert end == cliff + DFP * 10

    calc_endtime = vestingmath.getEndTime(cliff, amountPerPeriod, total)
    assert calc_endtime == cliff + 10 * DFP

    assert calc_endtime > current

    assert amountPerPeriod == 100

    vestingbucket = VestingBucket.deploy(
        token, cliff, numperiods, total, {"from": accounts[0]}
    )
    assert vestingbucket.totalAmount() == total

    untilend = vestingbucket.endTime() - current
    assert untilend == 20 * DFP
    chain.mine(timestamp=untilend)


def test_claimend(accounts, vestingmath, token):
    # test vest at end of the time
    DFP = vestingmath.DEFAULT_PERIOD()
    cliff = chain.time() + 1 * DFP
    numperiods = 10
    total = 1000
    vestingbucket = VestingBucket.deploy(
        token, cliff, numperiods, total, {"from": accounts[0]}
    )

    chain.sleep(DFP * 2)
    ct = chain.time()
    tilend = vestingbucket.endTime() - ct
    assert int(tilend / DFP) == 9


def test_claimendodd(accounts, vestingmath, token):
    DFP = vestingmath.DEFAULT_PERIOD()
    cliff = chain.time() + 1 * DFP
    numperiods = 10
    total = 1011
    vestingbucket = VestingBucket.deploy(
        token, cliff, numperiods, total, {"from": accounts[0]}
    )

    claimed = 0
    ct = chain.time()
    #assert vestingbucket.endTime() - ct == 12 * DFP


def test_claimendadd(accounts, vestingmath, token):
    # test vest at end of the time
    a = accounts[0]
    a2 = accounts[1]
    DFP = vestingmath.DEFAULT_PERIOD()
    cliff = chain.time() + 1 * DFP
    numperiods = 10
    total = 1000
    vestingbucket = VestingBucket.deploy(
        token, cliff, numperiods, total, {"from": accounts[0]}
    )

    # assert vestingbucket.endTime()-ct==11*DFP

    token.transfer(vestingbucket, 1000)
    vestingbucket.addClaim(a2, 1000, {"from": a})
    chain.mine(timestamp=cliff)

    # tt = vestingbucket.vestClaimMax(a, {'from': a})
    before = token.balanceOf(a2)
    vestingbucket.vestClaimMax(a2, {"from": a})
    after = token.balanceOf(a2)
    # assert tt > 0
    ca = vestingbucket.claimAddresses(0)
    assert vestingbucket.totalWithdrawnAmount() == 100
    assert vestingbucket.claims(ca)["claimAddress"] == ca
    assert vestingbucket.claims(ca)["claimAddress"] == a2
    assert vestingbucket.claims(ca)["withdrawnAmount"] == 100
    assert after - before == 100

    for n in range(1, 10):
        chain.mine(timestamp=cliff + DFP * n)
        before = token.balanceOf(a2)
        vestingbucket.vestClaimMax(a2, {"from": a})
        after = token.balanceOf(a2)
        assert vestingbucket.totalWithdrawnAmount() == 100 * n
        assert after - before == 100

    after = token.balanceOf(a2)
    assert after == 1000

    assert token.balanceOf(vestingbucket) == 0


def test_claimendadd(accounts, vestingmath, token):
    # test vest at end of the time
    a = accounts[0]
    a2 = accounts[1]
    DFP = vestingmath.DEFAULT_PERIOD()
    cliff = chain.time() + 1 * DFP
    numperiods = 10
    total = 1050
    vestingbucket = VestingBucket.deploy(
        token, cliff, numperiods, total, {"from": accounts[0]}
    )

    token.transfer(vestingbucket, total)
    vestingbucket.addClaim(a2, total, {"from": a})
    chain.mine(timestamp=cliff)

    before = token.balanceOf(a2)
    vestingbucket.vestClaimMax(a2, {"from": a})
    after = token.balanceOf(a2)
    ca = vestingbucket.claimAddresses(0)
    assert vestingbucket.totalWithdrawnAmount() == 105
    assert vestingbucket.claims(ca)["claimAddress"] == ca
    assert vestingbucket.claims(ca)["claimAddress"] == a2
    assert vestingbucket.claims(ca)["withdrawnAmount"] == 105
    assert after - before == 105

    for n in range(1, 9):
        chain.mine(timestamp=cliff + DFP * n)
        before = token.balanceOf(a2)
        vestingbucket.vestClaimMax(a2, {"from": a})
        after = token.balanceOf(a2)
        assert after - before == 105

    # assert token.balanceOf(vestingbucket) == 33

    chain.mine(timestamp=cliff + DFP * 11)
    before = token.balanceOf(a2)
    vestingbucket.vestClaimMax(a2, {"from": a})
    after = token.balanceOf(a2)
    assert after - before == 105

    assert after == 1050

    assert token.balanceOf(vestingbucket) == 0

    # x = vestingbucket.getVestableAmountAll()


def test_claimalltwo(accounts, vestingmath, token):
    # test allClaim
    a = accounts[0]
    a2 = accounts[1]
    a3 = accounts[2]
    DFP = vestingmath.DEFAULT_PERIOD()
    cliff = chain.time() + 1 * DFP
    numperiods = 10
    total = 1000
    vestingbucket = VestingBucket.deploy(
        token, cliff, numperiods, total, {"from": accounts[0]}
    )

    token.transfer(vestingbucket, 1000)
    vestingbucket.addClaim(a2, 600, {"from": a})
    vestingbucket.addClaim(a3, 400, {"from": a})
    chain.mine(timestamp=cliff)

    for n in range(0, 10):
        chain.mine(timestamp=cliff + DFP * n)
        vestingbucket.vestClaimMax(a2, {"from": a2})
        vestingbucket.vestClaimMax(a3, {"from": a3})
        assert vestingbucket.totalWithdrawnAmount() == 100 * (n + 1)

    after = token.balanceOf(a2)
    assert after == 600

    after = token.balanceOf(a3)
    assert after == 400

    assert token.balanceOf(vestingbucket) == 0


def test_unlcaimed(accounts, vestingmath, token):
    # test if claim misses a period
    a = accounts[0]
    a2 = accounts[1]
    a3 = accounts[2]
    DFP = vestingmath.DEFAULT_PERIOD()
    cliff = chain.time() + 1 * DFP
    numperiods = 10
    total = 1000
    vestingbucket = VestingBucket.deploy(
        token, cliff, numperiods, total, {"from": accounts[0]}
    )

    token.transfer(vestingbucket, 1000)
    vestingbucket.addClaim(a2, 1000, {"from": a})
    chain.mine(timestamp=cliff)

    n = 5
    chain.mine(timestamp=cliff + DFP * n)
    before = token.balanceOf(a2)
    vestingbucket.vestClaimMax(a2, {"from": a2})
    after = token.balanceOf(a2)
    assert after - before == 600

    assert token.balanceOf(vestingbucket) == 400
