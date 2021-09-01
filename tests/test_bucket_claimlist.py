
#!/usr/bin/python3

import pytest
from brownie import chain
import brownie



def test_claim_list(token, realbucket, claimlist, accounts):
    token.approve(realbucket, 1000, {"from": accounts[0]})
    assert token.allowance(accounts[0], realbucket) == 1000

    realbucket.depositOwner(1000)

    claimlist.addItem(accounts[0], 100)
    
    realbucket.addClaimsBatch(claimlist)

    assert realbucket.openClaimAmount() == 100

def test_claim_list_many(token, realbucket, claimlist, accounts):
    token.approve(realbucket, 10000, {"from": accounts[0]})
    assert token.allowance(accounts[0], realbucket) == 10000

    realbucket.depositOwner(10000)

    for i in range(10):
        claimlist.addItem(accounts[i], 100)
    
    realbucket.addClaimsBatch(claimlist)

    assert realbucket.openClaimAmount() == 1000

    realbucket.vestAll()

    assert realbucket.openClaimAmount() == 1000
    # assert realbucket.openClaimAmount() == 0