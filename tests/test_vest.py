#!/usr/bin/python3

from brownie.network.state import TxHistory
import pytest
from brownie import chain, Bucket
import brownie
import time


def test_claim_list_many(token, claimlist, accounts):
    t = chain.time()
    cliff = t + 1
    nump = 1
    total = 100
    p = 1
    bucket = Bucket.deploy(
        "Realbucket", token.address, cliff, nump, total, p, {"from": accounts[0]}
    )
    bucket.initialize()

    token.approve(bucket, 1000, {"from": accounts[0]})
    bucket.depositOwner(1000)

    bucket.addClaim(accounts[0], 100)

    c = bucket.claims(accounts[0])
    assert c == (accounts[0], 100, 100, 0, True)

    chain.sleep(p)

    assert bucket.openClaimAmount() == 100

    bucket.vestAll()

    assert bucket.openClaimAmount() == 0

    assert bucket.cliffTime() == cliff
    assert bucket.endTime() > cliff
    assert bucket.endTime() - bucket.registerTime() == 2
    assert bucket.duration() == 1
