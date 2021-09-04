#!/usr/bin/python3

# from brownie import Token, accounts
from brownie import accounts

import pytest
from brownie import chain, VegaToken, Bucket, ClaimList
import time

def runall():

    print("main")
    print(accounts)
    token = VegaToken.deploy({"from": accounts[0]})
    # token = VegaToken.at("0xDe6D2D63b10c088263B55154638746bD1057312F")
    # print(token)
    print(chain.time())
    t = int(time.time())
    print(t)
    day = 86400
    x = chain.time()
    cliff = x + 100 # day
    nump = 10
    total = 100
    p = 1
    
    bucket = Bucket.deploy(
        "Somebucket", token.address, cliff, nump, total, p, {"from": accounts[0]}
    )
    bucket.initialize()
    print(bucket.openClaimAmount())

    token.approve(bucket, 1000, {"from": accounts[0]})
    bucket.depositOwner(1000)

    for i in range(1, 10):
        bucket.addClaim(accounts[i], 101)

    print(bucket.openClaimAmount())
    chain.sleep(days*30*(nump-1))
    bucket.vestClaimMax(accounts[1])
    print("before last ",token.balanceOf(accounts[1]))
    chain.sleep(days*1)
    bucket.vestClaimMax(accounts[1])
    print("?? ",token.balanceOf(accounts[1]))
    
    # chain.sleep(days*30*1)
    # bucket.vestClaimMax(accounts[1])
    # print("?? ",token.balanceOf(accounts[1]))
    # babi = bucket.abi
    # hs = hashlib.sha1(str(babi).encode('utf-8')).hexdigest()
    # print(hs)

    # Contract.from_abi("Token", "0x79447c97b6543F6eFBC91613C655977806CB18b0", abi)
    # bucket = Bucket.at("0x5c609Db3A64Fd1bD5d4dA467963090f88BE2574a")
    print(bucket.name())
    print(bucket.cliffTime())

    token.approve(bucket, 1000, {"from": accounts[0]})
    assert token.allowance(accounts[0], bucket) == 1000

    bucket.depositOwner(1000)

    bucket.addClaim(accounts[1], 200)
    bucket.addClaim(accounts[2], 300)
    bucket.addClaim(accounts[3], 500)

    chain.sleep(day)

    # assert bucket.totalClaimAmount() == 100

    # tx =bucket.getVestableAmount(accounts[1], {"from": accounts[1]})
    # tx =bucket.vestClaimMax(accounts[1], {"from": accounts[1]})
    # for ev in tx.events:
    #     print(ev)
        # print(ev["logstring"],":",ev["amount"])
    # print(dir(bucket.getVestableAmount(accounts[1])))
    assert bucket.totalClaimAmount() == 1000
    bucket.vestAll()
    assert bucket.totalClaimAmount() == 0



def main():

    token = VegaToken.at("0xDe6D2D63b10c088263B55154638746bD1057312F")
    bucket = Bucket.at("0x5c609Db3A64Fd1bD5d4dA467963090f88BE2574a")
    print(bucket.name())
    print(bucket.cliffTime())
    print(bucket.totalClaimAmount())

    print(token.balanceOf(accounts[0]))
    print(token.balanceOf(accounts[1]))
    print(token.balanceOf(accounts[2]))
