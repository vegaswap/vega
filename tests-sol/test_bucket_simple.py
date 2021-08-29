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

    # cant claim more than total
    with brownie.reverts("VESTINGBUCKET: can not claim more than total"):
        bucket.addClaim(a2, 2000)

    with brownie.reverts("VESTINGBUCKET: can not claim tokens that are not deposited"):
        bucket.addClaim(a2, 1000)

    # token.transfer(bucket, 1000)
    # assert token.balanceOf(bucket) == 1000

    token.approve(bucket, 1000)
    bucket.depositOwner(1000)

    bucket.addClaim(a2, 1000)

    with brownie.reverts("VESTINGBUCKET: claim at this address already exists"):
        bucket.addClaim(a2, 1000)

    assert bucket.endTime() > 0

    tx = bucket.vestClaimMax(a2)
    assert tx.events["Transfer"][0]["from"] == bucket.address
    assert tx.events["Transfer"][0]["to"] == a2

    # assert bucket.events == 0

    # c = bucket.claims(a2)
    token.balanceOf(a2) == 500
    # assert c.claimAddress == a2
    # assert c.claimTotalmount == 1000

    with brownie.reverts("VESTINGBUCKET: no amount claimed"):
        bucket.vestClaimMax(a2)

    assert token.balanceOf(bucket) == 500
    assert bucket.openClaimAmount() == 500
    with brownie.reverts("VESTINGBUCKET: no unclaimed amount to withdraw"):
        bucket.withdrawOwner(100)

    token.approve(bucket, 1000)
    bucket.depositOwner(1000)
    assert token.balanceOf(bucket) == 1500
    bucket.withdrawOwner(1000)
    assert token.balanceOf(bucket) == 500
    with brownie.reverts("VESTINGBUCKET: no unclaimed amount to withdraw"):
        bucket.withdrawOwner(10)

    # assert token.balanceOf(bucket) == 300

    # chain.sleep(zz)

    # rclaim = vestingbucket.claims(a2).dict()
    # assert rclaim != None
    # assert rclaim["claimAddress"] == a2
    # assert rclaim["claimTotalAmount"] == 1000