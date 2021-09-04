# #!/usr/bin/python3

import pytest
from brownie import chain, Bucket, ClaimList
import brownie
import time


def test_claim_list_manylist(token, accounts):
    pass
    #TODO
    # t = chain.time()
    # cliff = t + 1
    # nump = 1
    # total = 1000
    # p = 1
    # clist = ClaimList.deploy({"from": accounts[0]})
    # bucket = Bucket.deploy(
    #     "Somebucket", token.address, cliff, nump, total, p, {"from": accounts[0]}
    # )
    # bucket.initialize()
    # # -- deposit 1000
    # token.approve(bucket, 1000, {"from": accounts[0]})
    # bucket.depositOwner(1000)
    # assert bucket.openClaimAmount() == 0

    # for i in range(1, 10):
    #     clist.addItem(accounts[i], 100)
    # bucket.addClaimsBatch(clist)
    # assert bucket.openClaimAmount() == 900
    # day = 86400
    # chain.sleep(day * 1000)
    # # -- vestall
    # bucket.vestAll()
    # assert bucket.openClaimAmount() == 0
    # tb = 0
    # for i in range(1, 10):
    #     x = token.balanceOf(accounts[i])
    #     assert x == 100
    #     tb += x

    # # -- 900 vested
    # assert tb == 900
    # # -- 100 left
    # assert token.balanceOf(bucket) == 100