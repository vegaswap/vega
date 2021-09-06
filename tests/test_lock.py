#!/usr/bin/python3

from brownie.network.state import TxHistory
import pytest
from brownie import chain, Bucket, Lock
import brownie
import time


def test_lock(token, accounts):
    token.transfer(accounts[1],1000, {"from": accounts[0]})

    lock = Lock.deploy(
        "Testlock", token.address, 100, {"from": accounts[1]}
    )

    token.approve(lock, 1000, {"from": accounts[1]})
    lock.depositOwner(1000)

    chain.sleep(99)
    with brownie.reverts("BUCKET: not unlock time yet"):
        lock.unlock()

    chain.sleep(2)

    lock.unlock()

    assert token.balanceOf(lock) == 0
    assert token.balanceOf(accounts[1]) == 1000