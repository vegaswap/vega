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

    for x in range(0,nump):
        chain.sleep(days)
        bucket.vestAll()
        assert bucket.openClaimAmount() == 900 - (x+1)*90
        tb = 0
        for i in range(1, 10):
            b = token.balanceOf(accounts[i])
            assert b == (x+1)*10
            tb += b
        assert tb == (x+1)*90

    assert bucket.openClaimAmount() == 0

    assert token.balanceOf(bucket) == 100


def test_claim_list_odd(token, accounts):
    t = chain.time()
    cliff = t + 1
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
    print(amountPerPeriod)
    assert amountPerPeriod == int(1050/11)
    from vmath import ceildiv
    duration = p * ceildiv(total, amountPerPeriod)
    assert bucket.duration() ==duration
    assert bucket.endTime() == bucket.cliffTime() + bucket.duration()

    for x in range(0,nump):
        chain.sleep(days)
        tx = bucket.vestAll()        
        # assert bucket.openClaimAmount() == 819 - (x+1)*90
        tb = 0
        for i in range(1, 10):
            b = token.balanceOf(accounts[i])
            assert b == (x+1)*9
            tb += b
        assert tb == (x+1)*81

    assert bucket.openClaimAmount() == 0

    # for x in range(nump,nump+1):
        
    #     chain.sleep(days)
    #     assert bucket.openClaimAmount() ==11
    #     # with brownie.reverts():
    #     tx = bucket.vestAll()        
    #     #??
    #     # assert False
    #     # assert tx.events.keys() == None
    #     assert tx.events["Slog"][0]["foo"] == "vestableAmount"
    #     assert tx.events["Slog"][0]["amount"] == 9
    #     assert tx.events["Slog"][1]["foo"] == "cap"
    #     assert tx.events["Slog"][2]["foo"] == "withdrawmount"
    #     assert tx.events["Slog"][3]["foo"] == "totalAfterwithdraw"
    #     assert tx.events["Slog"][3]["amount"] == 90

    #     assert tx.events["WithdrawClaim"][0]["amount"] == 99

    #     # assert bucket.openClaimAmount() == 819 - (x+1)*90
    #     tb = 0
    #     for i in range(1, 10):
    #         b = token.balanceOf(accounts[i])
    #         assert b == (x+1)*9
    #         tb += b
    #     assert tb == (x+1)*81

    

    assert bucket.openClaimAmount() == 9

    assert token.balanceOf(bucket) == 100

