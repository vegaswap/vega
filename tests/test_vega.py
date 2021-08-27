#!/usr/bin/python3
import brownie

from brownie import VegaToken, accounts


def test_vega(accounts, token):
    a = accounts[0]

    maxs = 10 ** 9 * 10 ** 18
    assert token.name() == "VegaToken"
    assert token.symbol() == "VEGA"
    assert token.totalSupply() == maxs

    # assert token.circulatingSupply() == 0
    assert token.decimals() == 18

    assert token.balanceOf(a) == maxs
