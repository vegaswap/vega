#!/usr/bin/python3

import pytest
from brownie import chain
import brownie

def within(a, b):
    assert abs(a - b) < 5

def test_list(token, realbucket, claimlist, accounts):
    # token.approve(realbucket, 1000, {"from": accounts[0]})
    # assert token.allowance(accounts[0], realbucket) == 1000
    assert claimlist.count() == 0
    assert claimlist.amounts(0) == 0
    claimlist.addItem(accounts[0], 100)
    assert claimlist.count() == 1
    assert claimlist.amounts(0) == 100
    assert claimlist.addresses(0) == accounts[0]

    claimlist.addItem(accounts[1], 500)
    assert claimlist.count() == 2
    assert claimlist.amounts(1) == 500
    assert claimlist.addresses(1) == accounts[1]
    

