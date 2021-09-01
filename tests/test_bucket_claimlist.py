
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
