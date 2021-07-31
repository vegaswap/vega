#!/usr/bin/python3
import brownie

from brownie import chain, VegaToken, VestingBucket, accounts
import time

days = 60 * 60 * 24
days30 = days * 30


def test_addall(accounts, vestingmath, token):

    cliff = chain.time() + 1
    DFP = vestingmath.DEFAULT_PERIOD()
    total = 1000
    periods = 6
    vestingbucket = VestingBucket.deploy(
        token, cliff, periods, total, {"from": accounts[0]}
    )
    assert token.balanceOf(vestingbucket) == 0
    assert vestingbucket.totalAmount() == total

    token.transfer(vestingbucket, 2000)
    assert token.balanceOf(vestingbucket) == 2000

    chain.mine(timestamp=cliff + DFP * periods)

    tc = 0
    import random

    for i in range(1, 6):
        # r = random.randint(1, 1000)
        amount = 200
        vestingbucket.addClaim(accounts[i], amount)
        tc += amount

    total = 0
    for i in range(1, 6):
        a = accounts[i]
        vestingbucket.vestClaimMax(a, {"from": a})
        assert token.balanceOf(a) == 200

    assert token.balanceOf(vestingbucket) == 1000
    total_distributed = 0
    for i in range(1, 6):
        a = accounts[i]
        total_distributed += token.balanceOf(accounts[i])
    assert total_distributed == tc

    assert token.balanceOf(vestingbucket) == 1000

    # TODO test circulating is 1000
    # TODO test locked is 1000
