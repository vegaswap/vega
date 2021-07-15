#!/usr/bin/python3

import pytest


@pytest.fixture(scope="function", autouse=True)
def isolate(fn_isolation):
    # perform a chain rewind after completing each test, to ensure proper isolation
    # https://eth-brownie.readthedocs.io/en/v1.10.3/tests-pytest-intro.html#isolation-fixtures
    pass


@pytest.fixture(scope="module")
def token(VegaToken, accounts):
    return VegaToken.deploy({'from': accounts[0]})


@pytest.fixture(scope="module")
def master(VegaMaster, accounts):
    master_contract = VegaMaster.deploy({'from': accounts[0]})
    #print(master_contract.revert_msg)
    return master_contract


@pytest.fixture(scope="module")
def vestingmath(VestingMath, token, accounts):
    master = VestingMath.deploy({'from': accounts[0]})
    return master

# @pytest.fixture(scope="module")
# def vestingbucket(VestingMath, VestingBucket, token, accounts):
#     VestingMath.deploy({'from': accounts[0]})
#     cliff = 0
#     total = 10000
#     return VestingBucket.deploy(token, cliff, total, {'from': accounts[0]})
