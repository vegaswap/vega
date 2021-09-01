#!/usr/bin/python3

import pytest
from brownie import chain
import brownie


def within(a, b):
    assert abs(a - b) < 5


def test_claim(token, realbucket, accounts):
    token.approve(realbucket, 1000, {"from": accounts[0]})
    assert token.allowance(accounts[0], realbucket) == 1000

    with brownie.reverts("BUCKET: can not claim tokens that are not deposited"):
        realbucket.addClaim(accounts[1], 100)


def test_claim(token, realbucket, accounts):
    token.approve(realbucket, 1000, {"from": accounts[0]})
    assert token.allowance(accounts[0], realbucket) == 1000

    realbucket.depositOwner(1000)

    realbucket.addClaim(accounts[1], 100)

    assert realbucket.totalClaimAmount() == 100

    assert token.balanceOf(realbucket) == 1000
    with brownie.reverts("BUCKET: can't withdraw claimed amounts"):
        realbucket.withdrawOwner(1000)

    with brownie.reverts("BUCKET: added already"):
        realbucket.addClaim(accounts[1], 100)

    realbucket.addClaim(accounts[2], 900)

    with brownie.reverts("BUCKET: can't withdraw claimed amounts"):
        realbucket.withdrawOwner(1)

    assert realbucket.totalClaimAmount() == 1000
