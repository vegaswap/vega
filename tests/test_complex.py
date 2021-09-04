# #!/usr/bin/python3

import pytest
from brownie import chain, Bucket, ClaimList
import brownie
import time

def test_claim_list(token, realbucket, claimlist, accounts):
    token.approve(realbucket, 1000, {"from": accounts[0]})
    assert token.allowance(accounts[0], realbucket) == 1000

    realbucket.depositOwner(1000)

    claimlist.addItem(accounts[0], 100)

    realbucket.addClaimsBatch(claimlist)

    assert realbucket.openClaimAmount() == 100


def test_claim_list_manylist(token, accounts):
    t = chain.time()
    cliff = t + 1
    nump = 1
    total = 1000
    p = 1
    clist = ClaimList.deploy({"from": accounts[0]})
    bucket = Bucket.deploy(
        "Somebucket", token.address, cliff, nump, total, p, {"from": accounts[0]}
    )
    bucket.initialize()
    # -- deposit 1000
    token.approve(bucket, 1000, {"from": accounts[0]})
    bucket.depositOwner(1000)
    assert bucket.openClaimAmount() == 0

    for i in range(1, 10):
        clist.addItem(accounts[i], 100)
    bucket.addClaimsBatch(clist)
    assert bucket.openClaimAmount() == 900
    day = 86400
    chain.sleep(day * 1000)
    # -- vestall
    bucket.vestAll()
    assert bucket.openClaimAmount() == 0
    tb = 0
    for i in range(1, 10):
        x = token.balanceOf(accounts[i])
        assert x == 100
        tb += x

    # -- 900 vested
    assert tb == 900
    # -- 100 left
    assert token.balanceOf(bucket) == 100


def test_claim_list_many(token, accounts):
    t = chain.time()
    cliff = t + 1
    nump = 10
    total = 1000
    days = 86400
    default_period = 30 * days
    p = default_period
    bucket = Bucket.deploy(
        "Somebucket", token.address, cliff, nump, total, p, {"from": accounts[0]}
    )
    bucket.initialize()
    # -- deposit 1000
    token.approve(bucket, 1000, {"from": accounts[0]})
    bucket.depositOwner(1000)
    assert bucket.openClaimAmount() == 0

    for i in range(1, 10):
        bucket.addClaim(accounts[i], 100)

    assert bucket.openClaimAmount() == 900

    assert bucket.duration() ==10*default_period
    assert bucket.endTime() == bucket.cliffTime() + 10*default_period

    untilcliff = chain.time() - cliff
    chain.sleep(untilcliff+10)
    # assert chain.time() - cliff < 20

    for x in range(0,nump):
        tx = bucket.vestAll()
        assert tx.events["WithdrawClaim"][0]["claimAddress"] == accounts[1]
        assert tx.events["WithdrawClaim"][0]["amount"] == 10

        assert bucket.openClaimAmount() == 900 - (90*(x+1))
        assert bucket.totalClaimAmount() == 900
        assert bucket.totalWithdrawnAmount() == 90*(x+1)

        chain.sleep(default_period)

        # assert tx.events["WithdrawClaim"][0]["claimAddress"] == accounts[1]
        # assert tx.events["WithdrawClaim"][0]["amount"] == 10
        # assert bucket.openClaimAmount() == 900 - 90*x

    assert bucket.openClaimAmount() == 0
    assert token.balanceOf(bucket) == 100



def test_claim_list_odd(token, accounts):
    t = chain.time()
    cliff = t + 10
    nump = 11
    total = 1050
    days = 86400
    default_period = 30 * days
    p = default_period
    bucket = Bucket.deploy(
        "Somebucket", token.address, cliff, nump, total, p, {"from": accounts[0]}
    )
    bucket.initialize()

    # -- deposit 1000
    token.approve(bucket, 1000, {"from": accounts[0]})
    bucket.depositOwner(1000)
    assert bucket.openClaimAmount() == 0

    for i in range(1, 10):
        bucket.addClaim(accounts[i], 100)

    assert bucket.openClaimAmount() == 900

    amountPerPeriod = int(total / nump)
    assert amountPerPeriod == int(1050/11)
    duration = p * nump
    assert bucket.duration() ==duration
    assert bucket.endTime() == bucket.cliffTime() + bucket.duration()
    tocliff = bucket.cliffTime()-chain.time()
    chain.sleep(tocliff)
    tocliff = bucket.cliffTime()-chain.time()
    assert tocliff == 0

    for x in range(0,nump-1):    
        tx = bucket.vestAll()
        tb = 0
        for i in range(1, 10):
            b = token.balanceOf(accounts[i])
            assert b == (x+1)*9
            tb += b
        assert tb == (x+1)*81

        chain.sleep(default_period)

    chain.sleep(default_period)
    tx = bucket.vestAll()
    tb = 0
    for i in range(1, 10):
        b = token.balanceOf(accounts[i])
        assert b == 100
        tb += b
    assert tb == 900

    assert bucket.openClaimAmount() == 0




def test_claim_list_odd(token, accounts):
    t = chain.time()
    cliff = t + 10
    nump = 11
    total = 1050
    days = 86400
    default_period = 30 * days
    p = default_period
    bucket = Bucket.deploy(
        "Somebucket", token.address, cliff, nump, total, p, {"from": accounts[0]}
    )
    bucket.initialize()

    # -- deposit 1000
    token.approve(bucket, 1000, {"from": accounts[0]})
    bucket.depositOwner(1000)
    assert bucket.openClaimAmount() == 0

    clist1 = ClaimList.deploy({"from": accounts[0]})
    clist2 = ClaimList.deploy({"from": accounts[0]})
    for i in range(1, 5):
        clist1.addItem(accounts[i], 100)

    for i in range(5, 10):
        clist2.addItem(accounts[i], 100)

    bucket.addClaimsBatch(clist1)
    bucket.addClaimsBatch(clist2)

    assert bucket.openClaimAmount() == 900

    amountPerPeriod = int(total / nump)
    assert amountPerPeriod == int(1050/11)
    duration = p * nump
    assert bucket.duration() ==duration
    assert bucket.endTime() == bucket.cliffTime() + bucket.duration()
    tocliff = bucket.cliffTime()-chain.time()
    chain.sleep(tocliff)
    tocliff = bucket.cliffTime()-chain.time()
    assert tocliff == 0

    for x in range(0,nump-1):    
        tx = bucket.vestAll()
        tb = 0
        for i in range(1, 10):
            b = token.balanceOf(accounts[i])
            assert b == (x+1)*9
            tb += b
        assert tb == (x+1)*81

        chain.sleep(default_period)

    chain.sleep(default_period)
    tx = bucket.vestAll()
    tb = 0
    for i in range(1, 10):
        b = token.balanceOf(accounts[i])
        assert b == 100
        tb += b
    assert tb == 900

    assert bucket.openClaimAmount() == 0
    assert token.balanceOf(bucket) == 100


