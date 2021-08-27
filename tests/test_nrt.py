#!/usr/bin/python3

import pytest


@pytest.mark.parametrize("idx", range(5))
def test_initial_approval_is_zero(token, accounts, idx):
    assert token.allowance(accounts[0], accounts[idx]) == 0


def test_approve(nrt, accounts):
    assert nrt.owners()[0] == accounts[0]

    nrt.issue(accounts[1], 100, {"from": accounts[0]})
    assert nrt.issuedSupply() == 100
    assert nrt.outstandingSupply() == 100
    assert nrt.redeemedSupply() == 0
    # assert token.allowance(accounts[0], accounts[1]) == 10**19
