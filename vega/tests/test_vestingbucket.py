#!/usr/bin/python3
import brownie

from brownie import chain, VegaToken, VestingBucket, accounts
import time
from collections import OrderedDict


days = 60 * 60 * 24
days30 = days * 30


def test_basic(accounts, vestingmath, token):

    cliff = chain.time() + 100
    total = 1000
    period = 1
    vestingbucket = VestingBucket.deploy(
        token, cliff, period, total, {"from": accounts[0]}
    )
    assert vestingbucket.totalAmount() == total

    a = accounts[0]

    dec = token.decimals()
    assert dec == 18

    a2 = accounts[1]
    token.transfer(vestingbucket, 1000)
    assert token.balanceOf(vestingbucket) == 1000

    # cant claim more than total
    with brownie.reverts("VESTINGBUCKET: can not claim more than total"):
        vestingbucket.addClaim(a2, 2000)

    vestingbucket.addClaim(a2, 1000)

    zz = 100000
    chain.sleep(zz)

    rclaim = vestingbucket.claims(a2).dict()
    assert rclaim != None
    assert rclaim["claimAddress"] == a2
    assert rclaim["claimTotalAmount"] == 1000

    before = token.balanceOf(a2)

    vestingbucket.vestClaimMax(a2, {"from": a2})

    assert token.balanceOf(vestingbucket) == 0
    assert token.balanceOf(a2) == 1000

    after = token.balanceOf(a2)
    dif = after - before
    assert dif == 1000


def test_twoclaims(accounts, vestingmath, token):

    cliff = chain.time() + 100
    total = 1000
    period = 1
    vestingbucket = VestingBucket.deploy(
        token, cliff, period, total, {"from": accounts[0]}
    )
    assert vestingbucket.totalAmount() == total

    a = accounts[0]
    a2 = accounts[1]
    a3 = accounts[2]
    token.transfer(vestingbucket, 1000)
    assert token.balanceOf(vestingbucket) == 1000
    vestingbucket.addClaim(a2, 600)
    with brownie.reverts("VESTINGBUCKET: claim at this address already exists"):
        vestingbucket.addClaim(a2, 400)

    vestingbucket.addClaim(a3, 400)

    zz = 100000
    chain.sleep(zz)

    vestingbucket.vestClaimMax(a2, {"from": a2})
    vestingbucket.vestClaimMax(a3, {"from": a3})

    assert token.balanceOf(vestingbucket) == 0
    assert token.balanceOf(a2) == 600
    assert token.balanceOf(a3) == 400


def test_cliff(accounts, token):

    ts = 100
    cliff = chain.time() + ts
    total = 10000
    period = 10
    amountPerPeriod = total / period

    assert amountPerPeriod == 1000

    vestingbucket = VestingBucket.deploy(
        token, cliff, period, total, {"from": accounts[0]}
    )
    assert vestingbucket.totalAmount() == total

    a = accounts[0]

    dec = token.decimals()
    assert dec == 18

    a2 = accounts[1]
    token.transfer(vestingbucket, 10000)
    total = 2000
    vestingbucket.addClaim(a2, total)

    ca1 = vestingbucket.claimAddresses(0)

    claim1 = vestingbucket.claims(ca1)
    claim1d = claim1.dict()

    assert claim1d["claimAddress"] == a2

    # cant withdraw while cliff
    before = token.balanceOf(vestingbucket)
    with brownie.reverts("VESTINGBUCKET: no amount claimed"):
        vestingbucket.vestClaimMax.call(a2, {"from": a2})

    after = token.balanceOf(vestingbucket)
    dif = after - before
    assert dif == 0


def test_addall(accounts, vestingmath, token):

    cliff = chain.time() + 100
    total = 1000
    period = 6
    vestingbucket = VestingBucket.deploy(
        token, cliff, period, total, {"from": accounts[0]}
    )
    assert token.balanceOf(vestingbucket) == 0
    assert vestingbucket.totalAmount() == total

    token.transfer(vestingbucket, 2000)
    assert token.balanceOf(vestingbucket) == 2000

    tc = 0
    import random

    for i in range(1, 6):
        amount = 200
        vestingbucket.addClaim(accounts[i], amount)
        tc += amount

    zz = 1000000000
    chain.sleep(zz)

    total = 0
    for i in range(1, 6):
        a = accounts[i]
        vestingbucket.vestClaimMax(a, {"from": a})
        assert token.balanceOf(a) == 200

    assert token.balanceOf(vestingbucket) == 1000
    total_distributed = 0
    for i in range(1, 6):
        a = accounts[i]
        total_distributed += token.balanceOf(accounts[i])
    assert total_distributed == tc

    assert token.balanceOf(vestingbucket) == 1000


def test_vestableall(accounts, vestingmath, token):

    ts = 0
    cliff = chain.time() + 1
    total = 1000
    period = 1
    vestingbucket = VestingBucket.deploy(
        token, cliff, period, total, {"from": accounts[0]}
    )

    assert vestingbucket.totalAmount() == total

    ct = vestingbucket.getCurrentTime()
    assert ct > 1625902477

    blocktime = 1625902745

    endtime = vestingmath.getEndTime(cliff, 500, 1000)
    z = vestingmath.getVestedAmountTSX(blocktime, ct, 0, endtime, 500, 1)
    assert z == 500

    cliffTime = 1625902745
    endtime = 1631086745
    amountPerPeriod = 500
    totalAmount = 1000
    timeSinceCliff = blocktime - cliffTime
    validPeriodCount = int(timeSinceCliff / period + 1)
    potentialReturned = validPeriodCount * amountPerPeriod

    assert timeSinceCliff == 0

    r1 = vestingmath.getVestedAmountTSX(
        blocktime, cliffTime, endtime, amountPerPeriod, totalAmount, 1
    )

    assert r1 == 500

    # chain.sleep(endtime-chain.time()+1)
    # va = vestingbucket.getVestableAmountAll()
    # assert va == totalAmount


def test_claimother(accounts, vestingmath, token):

    a = accounts[0]
    cliff = chain.time() + 1
    total = 10000
    period = 6
    vestingbucket = VestingBucket.deploy(
        token, cliff, period, total, {"from": accounts[0]}
    )
    assert vestingbucket.totalAmount() == total

    blackhat_account = accounts[3]
    before = token.balanceOf(vestingbucket)
    with brownie.reverts("VESTINGBUCKET: can only call from claimaddress or owner"):
        vestingbucket.vestClaimMax(a, {"from": blackhat_account})

    after = token.balanceOf(vestingbucket)
    assert after == before


def test_claimother2(accounts, vestingmath, token):

    cliff = chain.time() + 1
    total = 10000
    period = 6
    vestingbucket = VestingBucket.deploy(
        token, cliff, period, total, {"from": accounts[0]}
    )
    assert vestingbucket.totalAmount() == total

    a = accounts[0]
    a2 = accounts[1]
    token.transfer(vestingbucket, 10000)
    with brownie.reverts("RefOwnable: caller is not the owner of refowner"):
        vestingbucket.addClaim(a2, 2000, {"from": a2})


def test_claim_second(accounts, vestingmath, token):
    a = accounts[0]
    a2 = accounts[1]
    cliff = chain.time() + 1
    total = 10000
    period = 6
    vestingbucket = VestingBucket.deploy(
        token, cliff, period, total, {"from": accounts[0]}
    )

    vestingbucket.addClaim(a2, 2000)
    with brownie.reverts("VESTINGBUCKET: claim at this address already exists"):
        vestingbucket.addClaim(a2, 2000)


def test_claimaddress(accounts, vestingmath, token):

    cliff = chain.time() + 1
    total = 10000
    period = 6
    vestingbucket = VestingBucket.deploy(
        token, cliff, period, total, {"from": accounts[0]}
    )
    assert vestingbucket.totalAmount() == total

    a = accounts[0]
    a2 = accounts[1]
    token.transfer(vestingbucket, 10000)
    vestingbucket.addClaim(a2, 2000, {"from": a})
    assert vestingbucket.claimAddresses(0) == a2.address


def test_returnarg(accounts, vestingmath, token):

    cliff = chain.time() + 100
    total = 1000
    period = 6
    vestingbucket = VestingBucket.deploy(
        token, cliff, period, total, {"from": accounts[0]}
    )
    assert token.balanceOf(vestingbucket) == 0
    assert vestingbucket.totalAmount() == total

    token.transfer(vestingbucket, 2000)
    assert token.balanceOf(vestingbucket) == 2000

    tc = 0

    for i in range(1, 6):
        amount = 200
        vestingbucket.addClaim(accounts[i], amount)
        tc += amount

    zz = 1000000000
    chain.sleep(zz)

    total = 0
    for i in range(1, 6):
        a = accounts[i]
        result_vested = vestingbucket.vestClaimMax(a, {"from": a})
        assert result_vested.events != 0
        assert result_vested.events[0]["value"] == 200

        # assert result_vested == 200

    assert token.balanceOf(vestingbucket) == 1000


# withdrawn = vestingbucket.vestClaimMax.call(a2, {'from': a2})
# withdrawtx = vestingbucket.vestClaimMax(a2, {'from': a2})

# tx = withdrawtx.info()
# assert tx.events != None
# TODO check events withdrawal
# assert withdrawn == 1000
