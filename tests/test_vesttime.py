#!/usr/bin/python3

from brownie.network.state import TxHistory
import pytest
from brownie import chain, Bucket
import brownie
import time


def test_claim_list_many(token, claimlist, accounts):
    t = chain.time()
    cliff = t + 1
    nump = 2
    total = 101
    days = 86400
    default_period = 30 * days
    bucket = Bucket.deploy(
        "Realbucket",
        token.address,
        cliff,
        nump,
        total,
        default_period,
        {"from": accounts[0]},
    )
    bucket.initialize()

    token.approve(bucket, 101, {"from": accounts[0]})
    bucket.depositOwner(101)

    assert token.balanceOf(bucket) == 101

    bucket.addClaim(accounts[1], 101)

    c = bucket.claims(accounts[1])
    assert c == (accounts[1], 101, 50, 0, True)

    chain.sleep(10)

    assert bucket.openClaimAmount() == 101

    assert bucket.cliffTime() == cliff
    assert bucket.endTime() > cliff
    # assert bucket.endTime() - bucket.registerTime() == 2
    assert bucket.duration() == default_period * 2

    tx = bucket.vestAll()
    assert tx.events["WithdrawClaim"][0]["claimAddress"] == accounts[1]
    assert tx.events["WithdrawClaim"][0]["amount"] == 50

    chain.sleep(default_period)
    tx = bucket.vestAll()
    assert tx.events["WithdrawClaim"][0]["claimAddress"] == accounts[1]
    assert tx.events["WithdrawClaim"][0]["amount"] == 51

    assert bucket.openClaimAmount() == 0
    assert token.balanceOf(accounts[1]) == 101
    assert token.balanceOf(bucket) == 0


def test_claim_list_first(token, claimlist, accounts):
    t = chain.time()
    cliff = t + 1
    nump = 2
    total = 101
    days = 86400
    default_period = 30 * days
    bucket = Bucket.deploy(
        "Realbucket",
        token.address,
        cliff,
        nump,
        total,
        default_period,
        {"from": accounts[0]},
    )
    bucket.initialize()

    token.approve(bucket, 101, {"from": accounts[0]})
    bucket.depositOwner(101)

    assert token.balanceOf(bucket) == 101

    bucket.addClaim(accounts[0], 101)

    c = bucket.claims(accounts[0])
    assert c == (accounts[0], 101, 50, 0, True)

    chain.sleep(default_period * 2)

    assert bucket.openClaimAmount() == 101
    assert bucket.cliffTime() == cliff
    assert bucket.endTime() > cliff
    assert bucket.duration() == default_period * 2

    tx = bucket.vestAll()
    assert bucket.openClaimAmount() == 0
    assert tx.events["WithdrawClaim"][0]["claimAddress"] == accounts[0]
    assert tx.events["WithdrawClaim"][0]["amount"] == 101
