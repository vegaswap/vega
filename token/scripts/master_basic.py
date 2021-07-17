#!/usr/bin/python3

import time
import pdb

import brownie

# from web3 import Web3
from brownie import web3

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


def main():
    print("*** deploy master script *** ")

    print("network ", brownie.network)

    print(" loaded accounts ")
    for a in accounts:
        print(a)

    # TODO security checks this is the right account
    # https://github.com/eth-brownie/brownie/pull/1104

    mainAccount = accounts[0]

    vestingmath = VestingMath.deploy({"from": mainAccount})

    # master = deploy_allocate(mainAccount)
    master_address = "0x602C71e4DAC47a042Ee7f46E0aee17F94A3bA0B6"
    master = VegaMaster.at(master_address)

    vbucket = VestingBucket.at(master.buckets(0))
    print("vbucket ", vbucket)

    # vbucket.addClaim(accounts[1], 1000 * 10 ** 18, {"from": mainAccount})
    now = chain.time()
    print("now ", now)
    print("vbucket.endTime() ", vbucket.endTime())
    untilend = vbucket.endTime() - now
    # assert untilend == 20 * DFP
    chain.mine(timestamp=untilend)

    # vestingmath.getVestedAmountTSX(now, )

    ca = vbucket.claimAddresses(0)
    claim = vbucket.claims(ca)
    vamount = vbucket.getVestedAmount(claim)
    print("vamount ", vamount)
    print("now ", now)
    assert vamount == 0

    # result_vested = vbucket.vestClaimMax(accounts[1], {"from": mainAccount})
    # assert result_vested == 0

    # print(accounts[1].address)
    # aa = web3.toChecksumAddress(accounts[1].address)
    # vbucket_w3 = web3.eth.contract(address=vbucket.address, abi=vbucket.abi)
    # tx = vbucket_w3.functions.addClaim(aa, 1000, transact={"from": mainAccount})
    # transact={'from': eth.accounts[1]
    # print("result ", tx)

    # master_w3 = web3.eth.contract(address=master_address, abi=master.abi)

    # vbucket_w3 = web3.eth.contract(address=VestingBucket.abi

    # print(masterw3.functions.vestClaimMax()
    # vestingbucket.functions.vestClaimMax(a, {"from": a}).transact()

    # w3.eth.contract(address=address, abi=abi)

    # print(type(master))
    # print(dir(master))
    # print(master.info())
    # print(master.get_method_object())
    token = VegaToken.at(master.vega_token())
    print("master ", master)

    ls = master.lockedSupply()
    ts = token.balanceOf(master)
    print("locked     ", ls)
    print("not locked ", ts)
    print("total      ", ls + ts)

    print("# buckets ", master.bucket_num())
