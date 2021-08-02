#!/usr/bin/python3
import brownie

from brownie import VegaToken, VestingBucket, accounts, chain

# from ../

def test_vegamaster_amounts(accounts, master, vconstants):
    assert vconstants.seedAmount() == 12500000
    amounts = [
        vconstants.seedAmount(),
        vconstants.privateAmount(),
        vconstants.publicAmount(),
        vconstants.publicAmountB(),
        vconstants.liqAmount(),
        vconstants.lprewardsAmount(),
        vconstants.lpgrantsAmount(),
        vconstants.ecoAmount(),
        vconstants.trademiningAmount(),
        vconstants.teamAmount(),
        vconstants.advisoryAmount(),
        vconstants.treasuryAmount()]
    assert sum (amounts) == 10**9

def test_vegamaster_basic(accounts, master, vconstants):
    a = accounts[0]

    # assert master.vega_token == None
    # assert master.vega_token == None
    token = VegaToken.at(master.vega_token())
    assert token != None
    dec = token.decimals()
    assert dec == 18

    now = chain.time()

    master.addVestingBucket(
        now + vconstants.seedCliff(),
        "SeedFunding",
        vconstants.seedPeriods(),
        vconstants.seedAmount() * (10 ** dec),
        {"from": a},
    )
    b = VestingBucket.at(master.buckets(0))
    x = token.balanceOf(b)
    assert x == b.totalAmount()


def test_vegamaster_tokens(accounts, master_allocated):
    a = accounts[0]

    token = VegaToken.at(master_allocated.vega_token())
    assert token != None
    dec = token.decimals()
    assert dec == 18

    assert token.totalSupply() == 10 ** 9 * 10 ** dec

    total = 0
    n = master_allocated.bucket_num()
    assert n == 12
    for i in range(n):
        b = VestingBucket.at(master_allocated.buckets(i))
        x = token.balanceOf(b)
        assert x == b.totalAmount()
        total += x
    
    #TODO!
    assert total == 10 ** 9 * 10 ** 18



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
