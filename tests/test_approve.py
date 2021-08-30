# #!/usr/bin/python3

import pytest
from setup_tests import *

# def test_basic(test_accounts, transactor, token, pk1):

# @pytest.mark.parametrize("idx", range(5))
# def test_initial_approval_is_zero(token, test_accounts, idx):
#     assert token.allowance(accounts[0], accounts[idx]) == 0

def test_approve(token, accounts, transactor):
    assert accounts
    f = token.f.approve(accounts[1].address, 10 ** 19)
    transactor.buildpush(f, accounts[0])
    assert token.f.allowance(accounts[0].address, accounts[1].address).call() == 10 ** 19


def test_modify_approve(token, accounts, transactor):
    f = token.f.approve(accounts[1].address, 10 ** 19) 
    transactor.buildpush(f, accounts[0])
    assert token.f.allowance(accounts[0].address, accounts[1].address).call() == 10 ** 19

    f = token.f.approve(accounts[1].address, 0) 
    transactor.buildpush(f, accounts[0])
    assert token.f.allowance(accounts[0].address, accounts[1].address).call() == 0

    f = token.f.approve(accounts[1].address, 5) 
    transactor.buildpush(f, accounts[0])
    assert token.f.allowance(accounts[0].address, accounts[1].address).call() == 5


# def test_revoke_approve(token, accounts):
#     token.approve(accounts[1], 10 ** 19, {"from": accounts[0]})
#     token.approve(accounts[1], 0, {"from": accounts[0]})

#     assert token.allowance(accounts[0], accounts[1]) == 0


# def test_approve_self(token, accounts):
#     token.approve(accounts[0], 10 ** 19, {"from": accounts[0]})

#     assert token.allowance(accounts[0], accounts[0]) == 10 ** 19


# def test_only_affects_target(token, accounts):
#     token.approve(accounts[1], 10 ** 19, {"from": accounts[0]})

#     assert token.allowance(accounts[1], accounts[0]) == 0


# def test_returns_true(token, accounts):
#     tx = token.approve(accounts[1], 10 ** 19, {"from": accounts[0]})

#     assert tx.return_value is True


# def test_approval_event_fires(accounts, token):
#     tx = token.approve(accounts[1], 10 ** 19, {"from": accounts[0]})

#     assert len(tx.events) == 1
#     assert tx.events["Approval"].values() == [accounts[0], accounts[1], 10 ** 19]
