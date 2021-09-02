#!/usr/bin/python3

import pytest
from brownie import chain, VegaToken, Bucket
import brownie
import time


def within(a, b):
    assert abs(a - b) < 5


def test_claim(accounts):

    token = VegaToken.deploy({"from": accounts[0]})
    t = int(chain.time())
    day = 86400
    
    # cliff = t + 100  # day
    # nump = 1
    # total = 1000
    # p = 1

    # bucket = Bucket.deploy(
    #     "Somebucket", token.address, cliff, nump, total, p, {"from": accounts[0]}
    # )
    # bucket.initialize()
    # assert bucket.name() == "Somebucket"

    # token.approve(bucket, 1500, {"from": accounts[0]})

    # bucket.depositOwner(1500)

    # bucket.addClaim(accounts[1], 200)
    # assert bucket.totalClaimAmount() == 200
    # assert bucket.openClaimAmount() == 200

    # bucket.addClaim(accounts[2], 300)
    # assert bucket.totalClaimAmount() == 500
    # assert bucket.openClaimAmount() == 500
    # bucket.addClaim(accounts[3], 500)
    # assert bucket.totalClaimAmount() == 1000
    # assert bucket.openClaimAmount() == 1000

    # chain.sleep(day * 10)

    # assert bucket.claimCount() == 3
    # assert bucket.claim_addresses(0) == accounts[1]
    # assert bucket.claim_addresses(1) == accounts[2]
    # assert bucket.claim_addresses(2) == accounts[3]

    # assert bucket.openClaimAmount() == 1000
    # with brownie.reverts():
    #     bucket.withdrawOwner(1000)

    # bucket.vestAll()

    # # assert bucket.totalClaimAmount() == 1000
    # assert bucket.openClaimAmount() == 0

    # b1 = token.balanceOf(accounts[0])
    # bucket.withdrawOwner(500)
    # b2 = token.balanceOf(accounts[0])
    # assert b2-b1==500

    # # assert bucket.getVestableAmount(accounts[1])==10
