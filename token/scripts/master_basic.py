#!/usr/bin/python3

from brownie import VegaToken, VestingMath, VegaMaster, VestingConstants, VestingBucket, BasicBucket, accounts

import time
import pdb


def allocate(master, token, a):

    vconstants = VestingConstants.deploy({'from': a})
    print(vconstants)

    amounts = [vconstants.seedAmount(),
               vconstants.privateAmount(),
               vconstants.publicAmount(),
               vconstants.liqAmount(),
               vconstants.lprewardsAmount(),
               vconstants.lpgrantsAmount(),
               vconstants.ecoAmount(),
               vconstants.trademiningAmount(),
               vconstants.teamAmount(),
               vconstants.advisoryAmount()]
    print(amounts)
    print(sum(amounts))
    rest = token.totalSupply()/10**18 - sum(amounts)
    print("rest ", rest)

    DECIMALS = token.decimals()
    master.addVestingBucket(
        vconstants.seedCliff(),
        "SeedFunding",
        vconstants.seedPeriods(),
        vconstants.seedAmount() * (10**DECIMALS)
    )

    master.addVestingBucket(
        vconstants.privateCliff(),
        "PrivateFunding",
        vconstants.privatePeriods(),
        vconstants.privateAmount() * (10**DECIMALS)
    )

    master.addVestingBucket(
        vconstants.publicCliff(),
        "PublicFunding",
        vconstants.publicPeriods(),
        vconstants.publicAmount() * (10**DECIMALS)
    )

    master.addVestingBucket(
        vconstants.liqCliff(),
        "Liquidity",
        vconstants.liqPeriods(),
        vconstants.liqAmount() * (10**DECIMALS)
    )

    master.addVestingBucket(
        vconstants.lpwRewardsCliff(),
        "LPrewards",
        vconstants.lprewardsPeriods(),
        vconstants.lprewardsAmount() * (10**DECIMALS)
    )

    master.addVestingBucket(
        vconstants.lpgrantsCliff(),
        "LPgrants",
        vconstants.lpgrantsPeriods(),
        vconstants.lpgrantsAmount() * (10**DECIMALS)
    )

    master.addVestingBucket(
        vconstants.ecoCliff(),
        "Ecosystem",
        vconstants.ecoPeriods(),
        vconstants.ecoAmount() * (10**DECIMALS)
    )

    master.addVestingBucket(
        vconstants.trademiningCliff(),
        "TradeMining",
        vconstants.trademiningPeriods(),
        vconstants.trademiningAmount() * (10**DECIMALS)
    )

    master.addVestingBucket(
        vconstants.teamCliff(),
        "Team",
        vconstants.teamPeriods(),
        vconstants.teamAmount() * (10**DECIMALS)
    )

    master.addVestingBucket(
        vconstants.advisoryCliff(),
        "Advisory",
        vconstants.advisorsPeriods(),
        vconstants.advisoryAmount() * (10**DECIMALS)
    )

    master.addVestingBucket(
        vconstants.treasuryCliff(),
        "Treasury",
        vconstants.treasuryPeriods(),
        vconstants.treasuryAmount() * (10**DECIMALS)
    )


def main():
    print("*** basic master script *** ")

    a = accounts[0]
    vestingmath = VestingMath.deploy({'from': a})
    # token = VegaToken.deploy({'from': a})
    try:
        # pdb.set_trace()
        master = VegaMaster.deploy({'from': a})
    except Exception as e:
        print(e)
        return

    ta = master.vega_token()
    token = VegaToken.at(ta)

    # print (master.depositAmount())

    print("# buckets ", master.bucket_num())

    token = VegaToken.at(master.vega_token())
    print(token.decimals())
    print("got max supply ", token.balanceOf(master) == token.totalSupply())
    print("allocate")
    print(token.balanceOf(master)/10**18)

    allocate(master, token, a)

    ls = master.lockedSupply()
    ts = token.balanceOf(master)
    print("locked     ", ls)
    print("not locked ", ts)
    print("total      ", ls+ts)

    print(master.bucket_num())

    # addClaims

    # total = 0
    # for i in range(master.bucket_num()):
    #     b = BasicBucket.at(master.buckets(i))
    #     x = token.balanceOf(b)
    #     p = round(x/master.lockedSupply(), 3)
    #     total += x
    #     print(i, b.name(), x/10**18, p)

    seedbucket = VestingBucket.at(master.buckets(0))
    acc = accounts[1]
    seedbucket.addClaim(acc, 2000000 * 10**18, {'from': a})
    claimed = seedbucket.totalClaimAmount()
    total = seedbucket.totalAmount()
    print(claimed, total, claimed/total)

    # print(token.balanceOf(master)/10**18)

    # print(token.balanceOf(master)/10**18 == 0)
