#!/usr/bin/python3

import pytest
from brownie import chain
import brownie

def within(a, b):
    assert abs(a - b) < 5


def test_basic(token, basicbucket, accounts):
    assert basicbucket.name() == "Somebucket"
    regtime = basicbucket.registerTime()
    within(regtime, chain.time())
    dur = basicbucket.duration()
    assert dur == 10
    cf = basicbucket.cliffTime()
    offset = cf - regtime
    # assert basicbucket.endTime() == regtime + dur + offset
    within(basicbucket.endTime(), regtime + dur + offset)


def test_real(token, realbucket, accounts):
    assert realbucket.name() == "Realbucket"
    regtime = realbucket.registerTime()
    within(regtime, chain.time())
    dur = realbucket.duration()
    p = realbucket.period()
    assert p == 86400 * 30
    assert dur == 10 * p
    cf = realbucket.cliffTime()
    offset = cf - regtime
    # assert basicbucket.endTime() == regtime + dur + offset
    within(realbucket.endTime(), regtime + dur + offset)


def test_deposit(token, realbucket, accounts):
    token.approve(realbucket, 1000, {"from": accounts[0]})
    assert token.allowance(accounts[0], realbucket) == 1000

    realbucket.depositOwner(1000)

    assert token.balanceOf(realbucket) == 1000
    realbucket.withdrawOwner(1000)

def test_depositwithdraw(token, realbucket, accounts):
    token.approve(realbucket, 1000, {"from": accounts[0]})
    realbucket.depositOwner(1000)
    assert token.balanceOf(realbucket) == 1000
    realbucket.withdrawOwner(1000)    
    assert token.balanceOf(realbucket) == 0

def test_depositallownace(token, realbucket, accounts):
    with brownie.reverts():
        realbucket.depositOwner(1000)

def test_withdrawfail(token, realbucket, accounts):
    with brownie.reverts():
        realbucket.withdrawOwner(1000)    

def test_withdraw(token, realbucket, accounts):
    token.approve(realbucket, 1000, {"from": accounts[0]})
    realbucket.depositOwner(1000)
    with brownie.reverts():
        realbucket.withdrawOwner(1000, {"from": accounts[1]})    
