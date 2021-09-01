
#!/usr/bin/python3

from brownie.network.state import TxHistory
import pytest
from brownie import chain, Bucket
import brownie
import time

def test_claim_list_many(token, claimlist, accounts):
    t = chain.time()
    cliff = t + 1
    nump = 1
    total = 100
    p = 1
    bucket = Bucket.deploy(
        "Realbucket", token.address, cliff, nump, total, p, {"from": accounts[0]}
    )
    bucket.initialize()

    token.approve(bucket, 1000, {"from": accounts[0]})
    bucket.depositOwner(1000)

    # claimlist.addItem(accounts[0], 100)    
    # bucket.addClaimsBatch(claimlist)
    bucket.addClaim(accounts[0], 100)

    c = bucket.claims(accounts[0])
    assert c == (accounts[0], 100, 100, 0, True)

    chain.sleep(1000)

    assert bucket.openClaimAmount() == 100

    # bucket.vestAll()

    # BUG!
    # assert bucket.openClaimAmount() == 0

    assert bucket.cliffTime() == cliff
    assert bucket.endTime() > cliff
    assert bucket.endTime() - bucket.registerTime() == 2
    assert bucket.duration() == 1

    # assert bucket.blockts() == int(chain.time())
    # assert bucket.blockts() == 100
    # x = bucket.blockts()
    # assert type(x) == brownie.network.transaction.TransactionReceipt
    # assert x.timestamp == chain.time()
    # assert x.status == 1

    # # chain.sleep(10)

    # assert bucket.blockts.call() == chain.time()

    # x = bucket.getVestableAmount(accounts[0])
    # assert type(x) == brownie.network.transaction.TransactionReceipt
    # endin = chain.time() - bucket.endTime()
    # assert  -  == 100

    

    # x = bucket.vestClaimMax(accounts[0])
    # assert x == 100

    # c = bucket.claims(accounts[0])
    # assert c == (accounts[0], 100, 100, 0, True)


    # token.approve(realbucket, 10000, {"from": accounts[0]})
    # assert token.allowance(accounts[0], realbucket) == 10000

    # realbucket.depositOwner(10000)

    # for i in range(10):
    #     claimlist.addItem(accounts[i], 100)
    
    # realbucket.addClaimsBatch(claimlist)

    # assert realbucket.openClaimAmount() == 1000

    # 

    # assert realbucket.openClaimAmount() == 1000
    # # assert realbucket.openClaimAmount() == 0