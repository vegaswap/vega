#!/usr/bin/python3

import time
import pdb

import brownie

from brownie import (
    VegaToken,
    VestingMath,
    VegaMaster,
    VestingConstants,
    VestingBucket,
    accounts,
)


def get_invfile():
    with open("invdb.csv", "r") as f:
        lines = f.readlines()
    return lines


def get_inv():
    lines = get_invfile()
    start = 3
    claims = list()
    for line in lines[start:]:
        line = line.replace("\n", "")
        arr = line.split(",")
        amount, addr = int(arr[0]), arr[1]
        claims.append([addr, amount])

    return claims


def allocate(master, token, vconstants, mainAccount):
    print("allocate to buckets")

    # print(vconstants)

    amounts = [
        vconstants.seedAmount(),
        vconstants.privateAmount(),
        vconstants.publicAmount(),
        vconstants.liqAmount(),
        vconstants.lprewardsAmount(),
        vconstants.lpgrantsAmount(),
        vconstants.ecoAmount(),
        vconstants.trademiningAmount(),
        vconstants.teamAmount(),
        vconstants.advisoryAmount(),
    ]
    print(amounts)
    print(sum(amounts))
    rest = token.totalSupply() / 10 ** 18 - sum(amounts)
    print("rest ", rest)

    DECIMALS = token.decimals()
    master.addVestingBucket(
        vconstants.seedCliff(),
        "SeedFunding",
        vconstants.seedPeriods(),
        vconstants.seedAmount() * (10 ** DECIMALS),
    )

    master.addVestingBucket(
        vconstants.privateCliff(),
        "PrivateFunding",
        vconstants.privatePeriods(),
        vconstants.privateAmount() * (10 ** DECIMALS),
    )

    master.addVestingBucket(
        vconstants.publicCliff(),
        "PublicFunding",
        vconstants.publicPeriods(),
        vconstants.publicAmount() * (10 ** DECIMALS),
    )

    master.addVestingBucket(
        vconstants.liqCliff(),
        "Liquidity",
        vconstants.liqPeriods(),
        vconstants.liqAmount() * (10 ** DECIMALS),
    )

    master.addVestingBucket(
        vconstants.lpwRewardsCliff(),
        "LPrewards",
        vconstants.lprewardsPeriods(),
        vconstants.lprewardsAmount() * (10 ** DECIMALS),
    )

    master.addVestingBucket(
        vconstants.lpgrantsCliff(),
        "LPgrants",
        vconstants.lpgrantsPeriods(),
        vconstants.lpgrantsAmount() * (10 ** DECIMALS),
    )

    master.addVestingBucket(
        vconstants.ecoCliff(),
        "Ecosystem",
        vconstants.ecoPeriods(),
        vconstants.ecoAmount() * (10 ** DECIMALS),
    )

    master.addVestingBucket(
        vconstants.trademiningCliff(),
        "TradeMining",
        vconstants.trademiningPeriods(),
        vconstants.trademiningAmount() * (10 ** DECIMALS),
    )

    master.addVestingBucket(
        vconstants.teamCliff(),
        "Team",
        vconstants.teamPeriods(),
        vconstants.teamAmount() * (10 ** DECIMALS),
    )

    master.addVestingBucket(
        vconstants.advisoryCliff(),
        "Advisory",
        vconstants.advisorsPeriods(),
        vconstants.advisoryAmount() * (10 ** DECIMALS),
    )

    master.addVestingBucket(
        vconstants.treasuryCliff(),
        "Treasury",
        vconstants.treasuryPeriods(),
        vconstants.treasuryAmount() * (10 ** DECIMALS),
    )


def deploy_master(mainAccount):

    # vestingmath = VestingMath.deploy({"from": a})
    # token = VegaToken.deploy({'from': a})
    try:
        # pdb.set_trace()
        master = VegaMaster.deploy({"from": mainAccount})
    except Exception as e:
        print(e)
        return

    ta = master.vega_token()
    token = VegaToken.at(ta)
    print(token.balanceOf(master) / 10 ** 18)

    # print (master.depositAmount())

    print("# buckets ", master.bucket_num())

    token = VegaToken.at(master.vega_token())
    print(token.decimals())
    print("got max supply ", token.balanceOf(master) == token.totalSupply())


def main():
    print("*** deploy master script *** ")

    print("network ", brownie.network)

    print("allocate")

    mainAccount = accounts[0]

    # TODO security checks this is the right account
    # https://github.com/eth-brownie/brownie/pull/1104

    # deploy_master(mainAccount)

    vconstants = VestingConstants.deploy({"from": mainAccount})

    master_address = "0x8ffce6B66218529E618C2182902182eE5167a9Bc"
    master = VegaMaster.at(master_address)
    token = VegaToken.at(master.vega_token())

    # print(token.balanceOf(master))
    assert token.balanceOf(master) == token.totalSupply()

    print("# buckets ", master.bucket_num())

    allocate(master, token, mainAccount)

    # ls = master.lockedSupply()
    # ts = token.balanceOf(master)
    # print("locked     ", ls)
    # print("not locked ", ts)
    # print("total      ", ls + ts)

    # print(master.bucket_num())

    # # addClaims

    # # total = 0
    # # for i in range(master.bucket_num()):
    # #
    # #     x = token.balanceOf(b)
    # #     p = round(x/master.lockedSupply(), 3)
    # #     total += x
    # #     print(i, b.name(), x/10**18, p)

    # seedbucket = VestingBucket.at(master.buckets(0))
    # acc = accounts[1]
    # seedbucket.addClaim(acc, 2000000 * 10 ** 18, {"from": a})
    # claimed = seedbucket.totalClaimAmount()
    # total = seedbucket.totalAmount()
    # print(claimed, total, claimed / total)

    # # print(token.balanceOf(master)/10**18)

    # # print(token.balanceOf(master)/10**18 == 0)
