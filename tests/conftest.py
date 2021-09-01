#!/usr/bin/python3

import pytest
from brownie import chain, VegaToken, Bucket, ClaimList


@pytest.fixture(scope="function", autouse=True)
def isolate(fn_isolation):
    # perform a chain rewind after completing each test, to ensure proper isolation
    # https://eth-brownie.readthedocs.io/en/v1.10.3/tests-pytest-intro.html#isolation-fixtures
    pass


@pytest.fixture(scope="module")
def token(VegaToken, accounts):
    return VegaToken.deploy({"from": accounts[0]})

days = 86400
default_period = 30 * days

@pytest.fixture(scope="module")
def basicbucket(token, accounts):
    t = chain.time()
    cliff = t + 100
    nump = 10
    total = 100
    p = 1
    bucket = Bucket.deploy(
        "Somebucket", token.address, cliff, nump, total, p, {"from": accounts[0]}
    )
    bucket.initialize()
    return bucket

@pytest.fixture(scope="module")
def realbucket(token, accounts):
    t = chain.time()
    cliff = t + 100
    nump = 10
    total = 1000
    p = default_period
    bucket = Bucket.deploy(
        "Realbucket", token.address, cliff, nump, total, p, {"from": accounts[0]}
    )
    bucket.initialize()
    return bucket



@pytest.fixture(scope="module")
def claimlist(accounts):
    return ClaimList.deploy({"from": accounts[0]})
