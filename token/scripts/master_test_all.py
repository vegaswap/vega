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
    testaccount = accounts[1]

    now = chain.time()
    DFP = vestingmath.DEFAULT_PERIOD()
    print(now, DFP)

    # 1626509839
    # assert untilend == 20 * DFP
    # forward one month
    n = 2
    chain.mine(timestamp=now + DFP * n + 1)

    # vest all claims
    for i in range(1, 11):
        vbucket = VestingBucket.at(master.buckets(i))
        txr = vbucket.vestClaimMax(testaccount, {"from": testaccount})
        # txr = vested.dict()
        # txr._get_trace()
        print(txr.status)
        print(txr.txid)
        print(txr.timestamp)
        print(txr.value)

    # ['__annotations__', '__class__', '__delattr__', '__dict__', '__dir__',
    # '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__',
    #  '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__',
    # '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__',
    # '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__',
    #  '__weakref__', '_add_internal_xfer', '_await_confirmation',
    # '_await_transaction', '_call_cost', '_confirm_output', '_confirmed',
    # '_confirmed_trace', '_dev_revert_msg', '_error_string', '_events',
    #  '_expand_trace', '_full_name', '_get_trace', '_get_trace_gas',
    # '_internal_transfers', '_modified_state', '_new_contracts',
    # '_raise_if_reverted', '_raw_trace', '_return_value', '_revert_msg',
    #  '_revert_pc', '_reverted_trace', '_set_from_receipt', '_set_from_tx',
    # '_silent', '_source_string', '_subcalls', '_trace', '_trace_exc',
    # '_trace_origin', '_traceback_string', 'block_number', 'call_trace',
    # 'confirmations', 'contract_address', 'contract_name', 'coverage_hash',
    # 'dev_revert_msg', 'error', 'events', 'fn_name', 'gas_limit',
    #  'gas_price', 'gas_used', 'info', 'input', 'internal_transfers',
    # 'logs', 'modified_state', 'new_contracts', 'nonce', 'receiver',
    # 'replace', 'return_value', 'revert_msg', 'sender', 'source',
    # 'status', 'subcalls', 'timestamp', 'trace', 'traceback', 'txid',
    # 'txindex', 'value', 'wait']

    show_buckets(master, token)

    ta = token.balanceOf(testaccount)
    print(ta)

    # for i in range(1, 11):
    #     vbucket = VestingBucket.at(master.buckets(i))
    #     tc = vbucket.totalAmount()
    #     amount = tc  # 5000000 * 10 ** 18
    #     # print(vbucket.numClaims())
    #     # print(vbucket.totalClaimAmount())
    #     vbucket.addClaim(testaccount, amount, {"from": mainAccount})

    # vbucket = VestingBucket.at(master.buckets(0))
    # claimed = vbucket.totalClaimAmount() / 10 ** 18
    # total = vbucket.totalAmount() / 10 ** 18
    # print("claimed ", claimed)
    # print("total ", total)
    # print("p: ", claimed / total)
    # print(vbucket.numClaims())

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
