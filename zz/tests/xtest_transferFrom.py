# #!/usr/bin/python3
# import brownie

from setup_tests import *

def test_sender_balance_decreases(token, accounts, transactor):
    sender_balance = token.f.balanceOf(accounts[0].address).call()
    assert sender_balance == 10**9 * 10**18
    amount = sender_balance
    
    f1 = token.f.approve(accounts[1].address, amount)
    transactor.buildpush(f1, accounts[0])

    assert token.f.allowance(accounts[0].address, accounts[1].address).call() == amount

    f2 = token.f.transferFrom(accounts[0].address, accounts[2].address, amount)
    transactor.buildpush(f2, accounts[1])

    assert token.f.allowance(accounts[0].address, accounts[1].address).call() == 0

    assert token.f.balanceOf(accounts[0].address).call() == sender_balance - amount
    assert token.f.balanceOf(accounts[2].address).call() == amount


def test_sender_balance_decreases(token, accounts, transactor):
    sender_balance = token.f.balanceOf(accounts[0].address).call()
    amount = sender_balance

    token.approve(accounts[1], amount, {"from": accounts[0]})