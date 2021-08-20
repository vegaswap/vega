#!/usr/bin/python3

import pytest
import brownie
from brownie import (
    VegaIDO,
    MaxSupplyToken,
    accounts,
    chain,
)
import time

# def test_ido(accounts, token):
#     #token.approve(accounts[1], 10**19, {'from': accounts[0]})
#     #assert token.allowance(accounts[0], accounts[1]) == 10**19
#     vegatoken = token
#     a = accounts[0]
#     a2 = accounts[1]

#     assert vegatoken.totalSupply() == 10**9*10**18

#     investToken = MaxSupplyToken.deploy(1000, "Test Token", "TEST", {'from': a})
#     assert investToken.balanceOf(a) == 1000

#     price = 83
#     totalcap = 100000
#     capPerAccount = 1000
#     start = int(time.time())-10
#     end = start + 100000
#     # (address _investTokenAddress, uint256 _askpriceMultiple, uint256 _totalcap, uint256 _capPerAccount, uint256 _startTime, uint256 _endTime) {
#     # ido = VegaIDO.deploy(vegatoken.address,investToken.address, price, totalcap, start, end, {'from': a})
#     ido = VegaIDO.deploy(investToken.address, price, totalcap, capPerAccount, start, end, {'from': a})
#     assert ido

#     assert ido.totalcap() == totalcap
#     assert ido.capPerAccount() == capPerAccount
#     assert ido.askpriceMultiple() == price

#     with brownie.reverts("VegaIDO: not whitelisted"):
#         ido.invest(100,{'from': a2})    
    
#     # ido.addWhiteList([a2],[8300], {'from': a})
#     ido.addWhiteList([a2], {'from': a})

#     with brownie.reverts("VegaIDO: Please approve amount to invest"):
#         ido.invest(100,{'from': a2})

#     investToken.approve(ido.address, 100, {'from': a2})

#     investToken.transfer(a2, 100, {'from': a})
#     assert investToken.balanceOf(a2) == 100

#     # TODO
#     # with brownie.reverts("VegaIDO: out of stock"):
#     #     ido.invest(100, {'from': a2})

#     vegatoken.transfer(ido, 8300 ,{'from': a})
#     assert vegatoken.balanceOf(ido) == 8300

#     investToken.approve(ido.address, 100, {'from': a2})

#     #investToken.transfer(a2, 100, {'from': a})    

#     #TODO
#     # b1 = vegatoken.balanceOf(a)
#     # tx = ido.invest(100,{'from': a2})    
#     # assert tx.status==1
#     # assert vegatoken.balanceOf(a2) == 8300
#     # b2 = vegatoken.balanceOf(a)
#     # assert b2 - b1 == 8300


#     # #TODO
#     # b1 = vegatoken.balanceOf(a)
#     # ido.withDrawTokens(100, {'from': a})
#     # b2 = vegatoken.balanceOf(a)
#     # assert b2-b1 == 100
#     #withDrawFunding



