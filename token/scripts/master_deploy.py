#!/usr/bin/python3

import time
import pdb

import brownie

from scripts.allocate import *

from brownie import (
    VegaToken,
    VestingMath,
    VegaMaster,
    VestingConstants,
    VestingBucket,
    accounts,
    chain,
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


def deploy_master(mainAccount):
    print("+++ deploy master +++")

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

    return master


def deploy_allocate(mainAccount):

    vestingmath = VestingMath.deploy({"from": mainAccount})

    master = deploy_master(mainAccount)
    # master_address = "0x8ffce6B66218529E618C2182902182eE5167a9Bc"
    # master = VegaMaster.at(master_address)

    vconstants = VestingConstants.deploy({"from": mainAccount})
    print(vconstants.seedAmount())

    token = VegaToken.at(master.vega_token())

    # print(token.balanceOf(master))
    assert token.balanceOf(master) == token.totalSupply()

    print("allocate")

    allocate(master, token, vconstants, mainAccount)
    print("# buckets ", master.bucket_num())

    return master


def show_buckets(master, token):
    print("# buckets ", master.bucket_num())

    total = 0
    for i in range(master.bucket_num()):
        vbucket = VestingBucket.at(master.buckets(i))
        x = token.balanceOf(vbucket)
        p = round(x / master.lockedSupply(), 3)
        claimed = vbucket.totalClaimAmount() / 10 ** 18
        total += x
        print(i, vbucket.name(), x / 10 ** 18, p, claimed)

    print("\ntotal ", total)


def add_claims_test(master, mainAccount, testaccount):
    i = 0
    vbucket = VestingBucket.at(master.buckets(i))
    amount = 5000000 * 10 ** 18
    vbucket.addClaim(testaccount, amount, {"from": mainAccount})


def main():
    print("*** deploy master script *** ")

    print("network ", brownie.network)

    print(" loaded accounts ")
    for a in accounts:
        print(a)

    # TODO security checks this is the right account
    # https://github.com/eth-brownie/brownie/pull/1104

    mainAccount = accounts[0]
    # master = deploy_allocate(mainAccount)
    master_address = "0xDae02e4fE488952cFB8c95177154D188647a0146"
    master = VegaMaster.at(master_address)
    token = VegaToken.at(master.vega_token())
    print("master ", master)

    ls = master.lockedSupply()
    ts = token.balanceOf(master)
    print("locked     ", ls)
    print("not locked ", ts)
    print("total      ", ls + ts)

    print("# buckets ", master.bucket_num())

    show_buckets(master, token)
