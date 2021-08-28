#!/usr/bin/python3
import brownie

from brownie import chain, VegaToken, VestingBucket, accounts
import time
from collections import OrderedDict


days = 60 * 60 * 24
days30 = days * 30


def test_basic(accounts, token):

    # cliff = chain.time() + 100
    cliff = chain.time()
    total = 1000
    period = 2
    bucket = VestingBucket.deploy(
        token, cliff, period, total, {"from": accounts[0]}
    )
    assert bucket.totalAmount() == total

    a = accounts[0]

    dec = token.decimals()
    assert dec == 18

    a2 = accounts[1]
    
    token.approve(bucket, 1000)
    bucket.depositOwner(1000)

    bucket.addClaim(a2, 1000)

    with brownie.reverts("VESTINGBUCKET: claim at this address already exists"):
        bucket.addClaim(a2, 1000)

    assert bucket.endTime() > 0

