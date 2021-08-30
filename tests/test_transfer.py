# #!/usr/bin/python3
# import brownie

from setup_tests import *

def test_sender_balance_decreases(token, accounts, transactor):
    sender_balance = token.f.balanceOf(accounts[0].address).call()
    amount = sender_balance 

    f = token.f.transfer(accounts[1].address, amount) #, {"from": accounts[0]})
    transactor.buildpush(f, accounts[0])

    assert token.f.balanceOf(accounts[0].address).call() == sender_balance - amount


def test_receiver_balance_increases(token,accounts, transactor):
    receiver_balance = token.f.balanceOf(accounts[1].address).call()
    amount = token.f.balanceOf(accounts[0].address).call()

    f = token.f.transfer(accounts[1].address, amount)
    transactor.buildpush(f, accounts[0])

    assert token.f.balanceOf(accounts[1].address).call() == receiver_balance + amount


def test_total_supply_not_affected(accounts, token, transactor):
    total_supply = token.f.totalSupply().call()
    amount = token.f.balanceOf(accounts[0].address).call()

    f = token.f.transfer(accounts[1].address, amount)
    transactor.buildpush(f, accounts[0])

    assert token.f.totalSupply().call() == total_supply


# def test_returns_true(accounts, token):
#     amount = token.balanceOf(accounts[0])
#     tx = token.transfer(accounts[1], amount, {"from": accounts[0]})

#     assert tx.return_value is True


def test_transfer_full_balance(accounts, token, transactor):
    amount = token.f.balanceOf(accounts[0].address).call()
    receiver_balance = token.f.balanceOf(accounts[1].address).call()

    f = token.f.transfer(accounts[1].address, amount)
    transactor.buildpush(f, accounts[0])

    assert token.f.balanceOf(accounts[0].address).call() == 0
    assert token.f.balanceOf(accounts[1].address).call() == receiver_balance + amount


def test_transfer_zero_tokens(accounts, token, transactor):
    sender_balance = token.f.balanceOf(accounts[0].address).call()
    receiver_balance = token.f.balanceOf(accounts[1].address).call()

    f = token.f.transfer(accounts[1].address, 0)
    transactor.buildpush(f, accounts[0])

    assert token.f.balanceOf(accounts[0].address).call() == sender_balance
    assert token.f.balanceOf(accounts[1].address).call() == receiver_balance


def test_transfer_to_self(accounts, token, transactor):
    sender_balance = token.f.balanceOf(accounts[0].address).call()
    amount = sender_balance

    f = token.f.transfer(accounts[0].address, amount)
    transactor.buildpush(f, accounts[0])

    assert token.f.balanceOf(accounts[0].address).call() == sender_balance


def test_insufficient_balance(accounts, token, transactor):
    balance = token.f.balanceOf(accounts[0].address).call()

    # with brownie.reverts():
    f = token.f.transfer(accounts[1].address, balance + 1)
    #TODO
    # txr = transactor.buildpush(f, accounts[0])
    # assert txr

#TODO
# def test_transfer_event_fires(accounts, token):
#     amount = token.balanceOf(accounts[0])
#     tx = token.transfer(accounts[1], amount, {"from": accounts[0]})

#     assert len(tx.events) == 1
#     assert tx.events["Transfer"].values() == [accounts[0], accounts[1], amount]
