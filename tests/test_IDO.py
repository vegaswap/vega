#!/usr/bin/python3

import pytest
import brownie
from brownie import (
    VegaIDO,
    MaxSupplyToken,
    accounts,
    chain,
)


def test_basic(accounts, token):
    #token.approve(accounts[1], 10**19, {'from': accounts[0]})
    #assert token.allowance(accounts[0], accounts[1]) == 10**19
    vegatoken = token
    a = accounts[0]
    a2 = accounts[1]

    assert vegatoken.totalSupply() == 10**9*10**18

    investToken = MaxSupplyToken.deploy(1000, "Test Token", "TEST", {'from': a})
    assert investToken.balanceOf(a) == 1000

    price = 83
    cap = 100000
    ido = VegaIDO.deploy(vegatoken.address,investToken.address, 18, price, cap, {'from': a})
    assert ido

    assert ido.cap() == cap
    assert ido.askPriceMultiple() == price

    with brownie.reverts("VegaIDO: Please approve amount to invest"):
        ido.invest(100)

    investToken.approve(ido.address, 100, {'from': a})

    with brownie.reverts("VegaIDO: out of stock"):
        ido.invest(100)

    vegatoken.transfer(ido, 8300 ,{'from': a})
    assert vegatoken.balanceOf(ido) == 8300

    investToken.approve(ido.address, 100, {'from': a2})

    investToken.transfer(a2, 100, {'from': a})

    ido.invest(100,{'from': a2})    
    assert vegatoken.balanceOf(a2) == 8300

