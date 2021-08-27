#!/usr/bin/python3
import brownie

from brownie import chain, VegaToken, VestingBucket, accounts
import time
from collections import OrderedDict


days = 60 * 60 * 24
days30 = days * 30


def test_basic(accounts, token):

    cliff = chain.time() + 100
    total = 1000
    period = 1
    vestingbucket = VestingBucket.deploy(
        token, cliff, period, total, {"from": accounts[0]}
    )
    assert vestingbucket.totalAmount() == total

    a = accounts[0]

    dec = token.decimals()
    assert dec == 18

    
    a2 = accounts[1]

    # cant claim more than total
    with brownie.reverts("VESTINGBUCKET: can not claim more than total"):
        vestingbucket.addClaim(a2, 2000)


    with brownie.reverts("VESTINGBUCKET: can not claim tokens that are not deposited"):
        vestingbucket.addClaim(a2, 1000)
    

    # token.transfer(vestingbucket, 1000)
    # assert token.balanceOf(vestingbucket) == 1000

    token.approve(vestingbucket, 1000)
    vestingbucket.depositOwner(1000)

    vestingbucket.addClaim(a2, 1000)

    # zz = 100000
    # chain.sleep(zz)

    # rclaim = vestingbucket.claims(a2).dict()
    # assert rclaim != None
    # assert rclaim["claimAddress"] == a2
    # assert rclaim["claimTotalAmount"] == 1000

    # before = token.balanceOf(a2)

    # vestingbucket.vestClaimMax(a2, {"from": a2})

    # assert token.balanceOf(vestingbucket) == 0
    # assert token.balanceOf(a2) == 1000

    # after = token.balanceOf(a2)
    # dif = after - before
    # assert dif == 1000
