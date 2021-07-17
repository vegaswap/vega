#!/usr/bin/python3
import brownie

from brownie import VegaToken, VestingBucket, VestingConstants, accounts
from brownie import chain


def test_endtime(accounts, vestingmath, token, master):

    a = accounts[0]

    token = VegaToken.at(master.vega_token())
    assert token != None

    DECIMALS = 18
    assert token.totalSupply() == 10 ** 9 * 10 ** DECIMALS

    vconstants = VestingConstants.deploy({"from": accounts[0]})

    assert vconstants.seedAmount() != 0

    now = chain.time()

    master.addVestingBucket(
        vconstants.seedCliff(),
        "SeedFunding",
        vconstants.seedPeriods(),
        vconstants.seedAmount() * (10 ** DECIMALS),
        {"from": accounts[0]},
    )

    vbucket = VestingBucket.at(master.buckets(0))
    print("vbucket ", vbucket)

    assert vconstants.seedPeriods() == 6
    assert vconstants.seedAmount() == 12500000
    DFP = vconstants.DEFAULT_PERIOD()
    assert DFP == 2592000

    dif = vbucket.endTime() - now
    # should be 6??
    assert dif / DFP == 7
    # assert vbucket.endTime() == 0
    # assert 18144000/2592000