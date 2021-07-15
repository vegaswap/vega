#!/usr/bin/python3

from os import terminal_size
from brownie import VegaToken, VestingMath, VegaMaster, BasicBucket, accounts

import time


def main():
    print("*** deployment *** ")

    # owner account should be multisig

    a = accounts[0]
    vestingmath = VestingMath.deploy({'from': a})
    master = VegaMaster.deploy({'from': a})

    # master will mint MAX_SUPPLY for himself
    #
    # master will deploy 11 buckets in constructor
    # master

    fundingAddress = 0xabc
    fundingAddress = 0xabc
    fundingAddress = 0xabc
    fundingAddress = 0xabc
    fundingAddress = 0xabc
    VegaMaster.getBucket("Funding").addClaim(
        fundingAddress, 10000/0.01, {'from': a})
    VegaMaster.getBucket("Funding").addClaim(
        fundingAddress, 20000/0.01, {'from': a})

    VegaMaster.getBucket("Advisors").addClaim(
        fundingAddress, 20000/0.01, {'from': a})

    VegaMaster.getBucket("Team").addClaim(
        fundingAddress, 20000/0.01, {'from': a})

    # development/marketing is discretionary
    # ecosystems
    # tradeMining
    # ecosystems
    # team
    # VegaMaster.getBucket().claimTo(teamBonus)

    # advisory

    # LATER
    # VegaMaster.getBucket("LiqMining").addClaim(
    #     liqAddress, amountAll, {'from': a})

    #     contract LiquidityMining {

    #     function mine(){
    #         if callers does XYZ transfer(100)
    #     }

    # }
    # liqmining = new LiquidityMining()
    # VegaMaster.getBucket().claimTo(liqmining)
