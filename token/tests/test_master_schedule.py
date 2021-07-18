#!/usr/bin/python3
import brownie

from brownie import VegaToken, VestingBucket, accounts

# from ../


def test_vegamaster_tokens(accounts, vestingmath, token, master):
    a = accounts[0]

    # assert master.vega_token == None
    # assert master.vega_token == None
    token = VegaToken.at(master.vega_token())
    assert token != None
    dec = token.decimals()
    assert dec == 18

    assert token.totalSupply() == 10 ** 9 * 10 ** dec
    # TODO
    try:
        master.allocate()
    except Exception as e:
        assert True

    total = 0
    n = master.bucket_num()
    assert n == 11
    for i in range(n):
        b = VestingBucket.at(master.buckets(i))
        x = token.balanceOf(b)
        total += x
    assert total == 100

    # assert master.circSupply() == 0

    # buc = master.buckets(0)
    # bb = AbstractBucket.at(buc)
    # assert bb.name() == "SeedFunding"
    # assert token.balanceOf(bb) == 12500000 * 10**dec

    # total = 0
    # for i in range(11):
    #     buc = master.buckets(i)
    #     bb = AbstractBucket.at(buc)
    #     bt = token.balanceOf(bb)
    #     total += bt

    # assert total == 10**9 * 10**18
    # * 10**dec

    # assert token.circulatingSupply() == 10

    # 125*10**6*(10**dec)
