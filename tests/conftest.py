#!/usr/bin/python3

import pytest

from brownie import (
    VegaToken,
    NRT,
    VestingBucket,
    accounts,
    chain,
)


@pytest.fixture(scope="function", autouse=True)
def isolate(fn_isolation):
    # perform a chain rewind after completing each test, to ensure proper isolation
    # https://eth-brownie.readthedocs.io/en/v1.10.3/tests-pytest-intro.html#isolation-fixtures
    pass


@pytest.fixture(scope="module")
def token(VegaToken, accounts):
    return VegaToken.deploy({"from": accounts[0]})


@pytest.fixture(scope="module")
def nrt(accounts):
    return NRT.deploy("NRT", "NRTx", "x", {"from": accounts[0]})


# def allocate(master, token, vconstants, mainAccount):
#     print("allocate to buckets")

#     amounts = [
#         vconstants.seedAmount(),
#         vconstants.privateAmount(),
#         vconstants.publicAmount(),
#         vconstants.publicAmountB(),
#         vconstants.liqAmount(),
#         vconstants.lprewardsAmount(),
#         vconstants.lpgrantsAmount(),
#         vconstants.ecoAmount(),
#         vconstants.trademiningAmount(),
#         vconstants.teamAmount(),
#         vconstants.advisoryAmount(),
#     ]
#     # print(amounts)
#     # print(sum(amounts))
#     # rest = token.totalSupply() / 10 ** 18 - sum(amounts)
#     # print("rest ", rest)

#     # now = getCurrentTime
#     now = chain.time()

#     DECIMALS = token.decimals()

#     master.addVestingBucket(
#         now + vconstants.seedCliff(),
#         "SeedFunding",
#         vconstants.seedPeriods(),
#         vconstants.seedAmount() * (10 ** DECIMALS),
#         {"from": mainAccount},
#     )

#     master.addVestingBucket(
#         now + vconstants.privateCliff(),
#         "PrivateFunding",
#         vconstants.privatePeriods(),
#         vconstants.privateAmount() * (10 ** DECIMALS),
#         {"from": mainAccount},
#     )

#     master.addVestingBucket(
#         now + vconstants.publicCliff(),
#         "PublicFunding",
#         vconstants.publicPeriods(),
#         vconstants.publicAmount() * (10 ** DECIMALS),
#         {"from": mainAccount},
#     )

#     master.addVestingBucket(
#         now + vconstants.publicCliff(),
#         "PublicFunding",
#         vconstants.publicPeriods(),
#         vconstants.publicAmountB() * (10 ** DECIMALS),
#         {"from": mainAccount},
#     )

#     master.addVestingBucket(
#         now + vconstants.liqCliff(),
#         "Liquidity",
#         vconstants.liqPeriods(),
#         vconstants.liqAmount() * (10 ** DECIMALS),
#         {"from": mainAccount},
#     )

#     master.addVestingBucket(
#         now + vconstants.lpwRewardsCliff(),
#         "LPrewards",
#         vconstants.lprewardsPeriods(),
#         vconstants.lprewardsAmount() * (10 ** DECIMALS),
#         {"from": mainAccount},
#     )

#     master.addVestingBucket(
#         now + vconstants.lpgrantsCliff(),
#         "LPgrants",
#         vconstants.lpgrantsPeriods(),
#         vconstants.lpgrantsAmount() * (10 ** DECIMALS),
#         {"from": mainAccount},
#     )

#     master.addVestingBucket(
#         now + vconstants.ecoCliff(),
#         "Ecosystem",
#         vconstants.ecoPeriods(),
#         vconstants.ecoAmount() * (10 ** DECIMALS),
#         {"from": mainAccount},
#     )

#     master.addVestingBucket(
#         now + vconstants.trademiningCliff(),
#         "TradeMining",
#         vconstants.trademiningPeriods(),
#         vconstants.trademiningAmount() * (10 ** DECIMALS),
#         {"from": mainAccount},
#     )

#     master.addVestingBucket(
#         now + vconstants.teamCliff(),
#         "Team",
#         vconstants.teamPeriods(),
#         vconstants.teamAmount() * (10 ** DECIMALS),
#         {"from": mainAccount},
#     )

#     master.addVestingBucket(
#         now + vconstants.advisoryCliff(),
#         "Advisory",
#         vconstants.advisorsPeriods(),
#         vconstants.advisoryAmount() * (10 ** DECIMALS),
#         {"from": mainAccount},
#     )

#     amount = vconstants.treasuryAmount()
#     #amount = restBalance
#     master.addVestingBucket(
#         now + vconstants.treasuryCliff(),
#         "Treasury",
#         vconstants.treasuryPeriods(),
#         amount * (10 ** DECIMALS),
#         {"from": mainAccount},
#     )


# def mock_claims(master, token, vconstants, mainAccount):

#     n = master_allocated.bucket_num()
#     assert n == 11
#     for i in range(n):
#         b = VestingBucket.at(master_allocated.buckets(i))
#         b.addClaim()


@pytest.fixture(scope="module")
def master_allocated(master, token, vconstants, accounts):
    mainAccount = accounts[0]
    # master_contract = VegaMaster.deploy({"from": mainAccount})

    allocate(master, token, vconstants, mainAccount)
    return master


# @pytest.fixture(scope="module")
# def vestingbucket(VestingMath, VestingBucket, token, accounts):
#     VestingMath.deploy({'from': accounts[0]})
#     cliff = 0
#     total = 10000
#     return VestingBucket.deploy(token, cliff, total, {'from': accounts[0]})
