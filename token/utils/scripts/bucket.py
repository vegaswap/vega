#!/usr/bin/python3

from brownie import chain, history, VegaToken, VestingMath, VegaMaster, VestingBucket, Bucket, accounts

import time


def main():
    print(len(accounts))

    a = accounts[0]
    vestingmath = VestingMath.deploy({'from': a})
    token = VegaToken.deploy({'from': a})
    #token = VegaToken.deploy({'from': a})
    cliff = 0
    total = 10000
    vestingbucket = VestingBucket.deploy(token, cliff, 6, total, {'from': a})
    print(vestingbucket)

    a1 = accounts[1]
    print(a1)
    #dec = token.decimals()
    #print (dec)
    #b = token.balanceOf(vestingbucket)
    b = token.balanceOf(a)
    print(b)

    print(dir(chain))
    print(chain.id)
    print(history)
    token.transfer(vestingbucket, 0, {'from': a})
    #vestingbucket.addClaim(a1, 2000)

    # withdrawn = vestingbucket.vestClaim(a1, 100, {'from': a1})
    # print (withdrawn, type(withdrawn))
