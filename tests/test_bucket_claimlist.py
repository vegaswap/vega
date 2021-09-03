#!/usr/bin/python3

# from tests.conftest import claimlist
import pytest
from brownie import chain, Bucket, ClaimList
import brownie


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
    nump = 1
    total = 1000
    p = 1
    bucket = Bucket.deploy(
        "Somebucket", token.address, cliff, nump, total, p, {"from": accounts[0]}
    )
    bucket.initialize()
    # -- deposit 1000
    token.approve(bucket, 1000, {"from": accounts[0]})
    bucket.depositOwner(1000)
    assert bucket.openClaimAmount() == 0

    bucket.addClaim(accounts[1], 200)
    for i in range(2, 10):
        bucket.addClaim(accounts[i], 100)

    assert bucket.openClaimAmount() == 1000
    day = 86400
    chain.sleep(day * 1000)
    # -- vestall
    bucket.vestAll()
    assert bucket.openClaimAmount() == 0
    tb = 0
    x = token.balanceOf(accounts[1])
    assert x == 200
    tb += x

    for i in range(2, 10):
        x = token.balanceOf(accounts[i])
        assert x == 100
        tb += x

    # -- 900 vested
    assert tb == 1000
    # -- 100 left
    assert token.balanceOf(bucket) == 0
