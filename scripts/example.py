from brownie import chain, VegaToken, Bucket, accounts
import hashlib
from brownie.network.contract import Contract

def main():
    token = VegaToken.deploy({"from": accounts[0]})
    t = chain.time()
    cliff = t + 100
    nump = 10
    total = 1050
    days = 86400
    default_period = 30 * days
    p = default_period
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