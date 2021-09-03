#!/usr/bin/python3

# from tests.conftest import claimlist
import pytest
from brownie import chain, Bucket, ClaimList
import brownie

def test_claim_list_many(token, accounts):

    # token = token.deploy({"from": accounts[0]})
    t = chain.time()
    cliff = t + 100
    nump = 10
    total = 1050
    days = 86400
    default_period = 30 * days
    p = default_period
    bucket = Bucket.deploy(
        "Somebucket", token.address, cliff, nump, total, p, {"from": accounts[0]}
    )
    bucket.initialize()
    print(bucket.openClaimAmount())

    token.approve(bucket, 1000, {"from": accounts[0]})
    bucket.depositOwner(1000)

    claimAmount = 101
    for i in range(1, 10):
        bucket.addClaim(accounts[i], 101)

    print(bucket.openClaimAmount())
    chain.sleep(days*30*(nump-1))
    bucket.vestClaimMax(accounts[1])
    bal1 = token.balanceOf(accounts[1])
    assert bal1 == 90
    print("before last ",)
    chain.sleep(days*1)

    # assert bucket.claims(accounts[1]).withdrawAmount == 0

    claim = bucket.claims(accounts[1])
    assert claim == (accounts[1], 101, 10, 90, True)

    chain.sleep(days*100)
    tx = bucket.vestClaimMax(accounts[1])
    assert tx.events["Slog"][0]["amount"] == 101
    assert tx.events["Slog"][1]["amount"] == 101
    assert tx.events["Slog"][2]["amount"] == 90
    assert tx.events["Slog"][3]["amount"] == 11
    assert tx.events["Slog"][4]["amount"] == 101
    bal = token.balanceOf(accounts[1])
    #BUG doesnt vest 101
    claim = bucket.claims(accounts[1])
    assert claim == (accounts[1], 101, 10, 101, True)
    # print("?? ",)
    assert bal == claimAmount

    # assert bal == claimAmount

    # t = chain.time()
    # cliff = t + 1
    # nump = 10
    # total = 1000
    # days = 86400
    # default_period = 30 * days
    # p = default_period
    # bucket = Bucket.deploy(
    #     "Somebucket", token.address, cliff, nump, total, p, {"from": accounts[0]}
    # )
    # bucket.initialize()
    # # -- deposit 1000
    # token.approve(bucket, 1000, {"from": accounts[0]})
    # bucket.depositOwner(1000)
    # assert bucket.openClaimAmount() == 0

    # for i in range(1, 10):
    #     bucket.addClaim(accounts[i], 100)

    # assert bucket.openClaimAmount() == 900

    # assert bucket.duration() ==10*default_period
    # assert bucket.endTime() == bucket.cliffTime() + 10*default_period

    # for x in range(0,nump):
    #     chain.sleep(days)
    #     bucket.vestAll()
    #     assert bucket.openClaimAmount() == 900 - (x+1)*90
    #     tb = 0
    #     for i in range(1, 10):
    #         b = token.balanceOf(accounts[i])
    #         assert b == (x+1)*10
    #         tb += b
    #     assert tb == (x+1)*90

    # assert bucket.openClaimAmount() == 0

    # assert token.balanceOf(bucket) == 100

