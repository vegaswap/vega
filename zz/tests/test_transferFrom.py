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


def test_receiver_balance_increases(token, accounts, transactor):
    sender_balance = token.f.balanceOf(accounts[0].address).call()
    amount = sender_balance

    f = token.f.approve(accounts[1].address, amount)
    transactor.buildpush(f, accounts[0])
    
    receiver_balance = token.f.balanceOf(accounts[2].address).call()
    amount = token.f.balanceOf(accounts[0].address).call()

    f = token.f.approve(accounts[1].address, amount)
    transactor.buildpush(f, accounts[0])

    f = token.f.transferFrom(accounts[0].address, accounts[2].address, amount)
    transactor.buildpush(f, accounts[1])

    assert token.f.balanceOf(accounts[2].address).call() == receiver_balance + amount


def test_caller_balance_not_affected(accounts, token, transactor):
    caller_balance = token.f.balanceOf(accounts[1].address).call()
    amount = token.f.balanceOf(accounts[0].address).call()

    f1 = token.f.approve(accounts[1].address, amount)
    transactor.buildpush(f1, accounts[0])
    f2 = token.f.transferFrom(accounts[0].address, accounts[2].address, amount)
    transactor.buildpush(f2, accounts[1])

    assert token.f.balanceOf(accounts[1].address).call() == caller_balance



def test_caller_approval_affected(accounts, token, transactor):
    approval_amount = token.f.balanceOf(accounts[0].address).call()
    transfer_amount = approval_amount

    f = token.f.approve(accounts[1].address, approval_amount)
    transactor.buildpush(f, accounts[0])
    f = token.f.transferFrom(accounts[0].address, accounts[2].address, transfer_amount)
    transactor.buildpush(f, accounts[1])

    assert (
        token.f.allowance(accounts[0].address, accounts[1].address).call() == approval_amount - transfer_amount
    )


def test_receiver_approval_not_affected(accounts, token, transactor):
    approval_amount = token.f.balanceOf(accounts[0].address).call()
    transfer_amount = approval_amount

    f = token.f.approve(accounts[1].address, approval_amount)
    transactor.buildpush(f, accounts[0])
    f = token.f.approve(accounts[2].address, approval_amount)
    transactor.buildpush(f, accounts[0])
    f = token.f.transferFrom(accounts[0].address, accounts[2].address, transfer_amount)
    transactor.buildpush(f, accounts[1])

    assert token.f.allowance(accounts[0].address, accounts[2].address).call() == approval_amount


def test_total_supply_not_affected(accounts, token, transactor):
    total_supply = token.f.totalSupply().call()
    amount = token.f.balanceOf(accounts[0].address).call()

    f = token.f.approve(accounts[1].address, amount)
    transactor.buildpush(f, accounts[0])
    f = token.f.transferFrom(accounts[0].address, accounts[2].address, amount)
    transactor.buildpush(f, accounts[1])

    assert token.f.totalSupply().call() == total_supply


# # def test_returns_true(accounts, token, transactor):
# #     amount = token.f.balanceOf(accounts[0].address).call()
# #     token.f.approve(accounts[1].address, amount, transactor.buildpush(f, accounts[0])
# #     tx = token.f.transferFrom(accounts[0].address, accounts[2].address, amount)
# transactor.buildpush(f, accounts[1])

# #     assert tx.return_value is True


def test_transfer_full_balance(accounts, token, transactor):
    amount = token.f.balanceOf(accounts[0].address).call()
    receiver_balance = token.f.balanceOf(accounts[2].address).call()

    f = token.f.approve(accounts[1].address, amount)
    transactor.buildpush(f, accounts[0])
    f = token.f.transferFrom(accounts[0].address, accounts[2].address, amount)
    transactor.buildpush(f, accounts[1])

    assert token.f.balanceOf(accounts[0].address).call() == 0
    assert token.f.balanceOf(accounts[2].address).call() == receiver_balance + amount


def test_transfer_zero_tokens(accounts, token, transactor):
    sender_balance = token.f.balanceOf(accounts[0].address).call()
    receiver_balance = token.f.balanceOf(accounts[2].address).call()

    f = token.f.approve(accounts[1].address, sender_balance)
    transactor.buildpush(f, accounts[0])
    f = token.f.transferFrom(accounts[0].address, accounts[2].address, 0)
    transactor.buildpush(f, accounts[1])

    assert token.f.balanceOf(accounts[0].address).call() == sender_balance
    assert token.f.balanceOf(accounts[2].address).call() == receiver_balance


def test_transfer_zero_tokens_without_approval(accounts, token, transactor):
    sender_balance = token.f.balanceOf(accounts[0].address).call()
    receiver_balance = token.f.balanceOf(accounts[2].address).call()

    f = token.f.transferFrom(accounts[0].address, accounts[2].address, 0)
    transactor.buildpush(f, accounts[1])

    assert token.f.balanceOf(accounts[0].address).call() == sender_balance
    assert token.f.balanceOf(accounts[2].address).call() == receiver_balance


def test_insufficient_balance(accounts, token, transactor):
    balance = token.f.balanceOf(accounts[0].address).call()

    f = token.f.approve(accounts[1].address, balance + 1)
    transactor.buildpush(f, accounts[0])
    #TODO
    # with brownie.reverts():
    # f = token.f.transferFrom(accounts[0].address, accounts[2].address, balance + 1)
    # tx = transactor.buildpush(f, accounts[1])
    # assert tx


def test_insufficient_approval(accounts, token, transactor):
    balance = token.f.balanceOf(accounts[0].address).call()

    f = token.f.approve(accounts[1].address, balance - 1)
    transactor.buildpush(f, accounts[0])
    #TODO
    # with brownie.reverts():
    #     token.f.transferFrom(accounts[0].address, accounts[2].address, balance)
    # transactor.buildpush(f, accounts[1])


# def test_no_approval(accounts, token, transactor):
#     balance = token.f.balanceOf(accounts[0].address).call()

    #TODO
#     with brownie.reverts():
#         token.f.transferFrom(accounts[0].address, accounts[2].address, balance)
# transactor.buildpush(f, accounts[1])


# # def test_revoked_approval(accounts, token, transactor):
# #     balance = token.f.balanceOf(accounts[0].address).call()

# #     token.f.approve(accounts[1].address, balance, transactor.buildpush(f, accounts[0])
# #     token.f.approve(accounts[1].address, 0, transactor.buildpush(f, accounts[0])
#TODO
# #     with brownie.reverts():
# #         token.f.transferFrom(accounts[0].address, accounts[2].address, balance)
# transactor.buildpush(f, accounts[1])


# def test_transfer_to_self(accounts, token, transactor):
#     sender_balance = token.f.balanceOf(accounts[0].address).call()
#     amount = sender_balance

#     f = token.f.approve(accounts[0].address, sender_balance)
#     transactor.buildpush(f, accounts[0])
#     token.f.transferFrom(accounts[0].address, accounts[0].address, amount)
#     transactor.buildpush(f, accounts[0])

#     assert token.f.balanceOf(accounts[0].address).call() == sender_balance
#     assert token.f.allowance(accounts[0].address, accounts[0].address).call() == sender_balance - amount


# # def test_transfer_to_self_no_approval(accounts, token, transactor):
# #     amount = token.f.balanceOf(accounts[0].address).call()

# #     with brownie.reverts():
# #         token.f.transferFrom(accounts[0].address, accounts[0].address, amount, transactor.buildpush(f, accounts[0])


# # def test_transfer_event_fires(accounts, token, transactor):
# #     amount = token.f.balanceOf(accounts[0].address).call()

# #     token.f.approve(accounts[1].address, amount, transactor.buildpush(f, accounts[0])
# #     tx = token.f.transferFrom(accounts[0].address, accounts[2].address, amount)
# transactor.buildpush(f, accounts[1])

# #     assert len(tx.events) == 1
# #     # assert len(tx.events) == 2
# #     assert tx.events["Transfer"].values() == [accounts[0].address, accounts[2].address, amount]
