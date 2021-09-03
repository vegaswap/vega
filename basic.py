import sys
import time
sys.path.insert(0, "../transactor")
from datetime import datetime, date

from eth_account import Account, account
from web3 import Web3
import toml
from pathlib import Path

from web3.types import SignedTx
import transact
from loguru import logger
import sys
import toml
import yaml
import json
import pytest

# with open("./build/contracts/Bucket.json","r") as f:
#     x = f.read()
#     z = json.loads(x)
#     print(z.keys())


with open("vconfig.yaml") as f:
    cfg = yaml.load(f, Loader=yaml.FullLoader)

def signpush(transactor, account, tx):
    signedtx = account.signTransaction(tx)
    tx_receipt = transactor.pushtx(signedtx)
    return tx_receipt

def signpush_deploy(transactor, account, tx):
    signedtx = account.signTransaction(tx)
    tx_receipt = transactor.pushtx(signedtx)
    return tx_receipt    

def deploy(acct, transactor, ctr, pk):
    dtx = transactor.get_deploy_tx(ctr, cargs=None)
    tx_receipt = signpush_deploy(transactor, acct, dtx)
    cta = tx_receipt["contractAddress"]
    return cta

def get_ctr(ctrname, accounts, pk1):
    myaddr = accounts[0].address

    transactor = transact.get_transactor("LOCAL", myaddr, cfg["builddir"], "")
    
    ctr = transactor.get_ctr(ctrname)
    print(ctr)
    cta = deploy(accounts[0], transactor, ctr, pk1)
    ctr = transactor.load_contract(cta, transactor.get_contract(ctrname).abi)
    return ctr    

pks = ["0x0fce4fd715a7a263cb127007cf8e685d1689e84ad8baa7a988ed3957f76a5d3a",
"0x5d54c9926bc807d9b450190dd779cecd8da19ef60c040eb02e6a5a48f3d152d0",
"0x3474a2dc495b0ae46b9ac1b81f67ec6a2acb3e9fe83634ad3f4caad1c43d0a76",
"0x9cb670120feb5e70ae7218acf2c2c061958f9c7b47ee11afc9c9671a147683db",
"0xce43593a1648024625db3d187098940d76786e39ce5563f9d0186e589219a860",
"0xb291b4f245fc722e3958a3138b7bf5256ebc4c7c7998dafc4d9c82f899f3acc6",
"0xf261312fe8819ac5a5bbda3432e9b228dc6b0c40ac8cc5d28c320fd6afe9c396",
"0x3c6b3b0122ebf9717207a7a7a3da7b5899d07b6f9cd793fd29d15e4e41a6eceb",
"0xbcf894fb1a3291a359f36244c2aaf80ea5db8a45faf7222f00fda576dcad0db8",
"0xb7600ce592e8cb536869a8142d63e5460321885134fa184cc92e04fb45bdd1bb"]


def accounts():
    a = list()
    for pk in pks:
        accounta = Account()
        acct = accounta.privateKeyToAccount(pk)
        a.append(acct)
    return a

def get_transactor(a):
    transactor = transact.get_transactor("LOCAL", a[0].address, cfg["builddir"], "")
    return transactor


def token(a, transactor):
    myaddr = a[0].address

    transactor = transact.get_transactor("LOCAL", myaddr, cfg["builddir"], "")
    ctrname = "VegaToken"
    ctr = transactor.get_ctr(ctrname)
    cta = deploy(a[0], transactor, ctr, pks[0])
    ctr = transactor.load_contract(cta, transactor.get_contract(ctrname).abi)
    return ctr

def deploy_token():
    a = accounts()
    tr = get_transactor(a)
    vtoken = token(a, tr)

def deploy_bucket(tr, vtoken, a):
    bucket_ctr = tr.get_ctr("Bucket")
    import time
    d = date(2021,9,4)
    unixtime = time.mktime(d.timetuple())
    # cliff = t+1000
    cliff = int(unixtime)
    print(cliff)
    num = 1
    total = 100
    p = 1
    cargs = ("BasicBucket", vtoken.address, cliff, num, total, p)
    dtx = tr.get_deploy_tx(bucket_ctr, cargs=cargs)
    tx_receipt = signpush_deploy(tr, a[0], dtx)
    cta = tx_receipt["contractAddress"]
    return cta

def increase_chaintime(seconds):
    # t = int(time.time())
    # 1630489405
    # ganache-cli -m vega --time '2021-09-01T15:53:00+00:0'
    try:
        method = "evm_increaseTime"
        # method = "evm_setTime"
        # start = 10000
        # args = [seconds]
        args = [seconds]
        response = tr.w3.provider.make_request(method, args)  # type: ignore
        print(response)
    except Exception as e:
        print(">> ",e)
        pass

def get_ts(ts):
    tsf = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    return tsf

def deposittokens():
    txp = tr.get_tx_params(200000)
    print("approve ", bucket.address)
    tx = vtoken.f.approve(bucket.address, 1000).buildTransaction(txp)
    signpush(tr, a[0], tx)

    #NOT WORKING?
    print(vtoken.f.allowance(a[0].address, bucket.address).call())
    txp = tr.get_tx_params(200000)
    tx = bucket.f.depositOwner(100).buildTransaction(txp)
    signpush(tr, a[0], tx)
    print(vtoken.f.balanceOf(a[0].address).call())
    print(vtoken.f.balanceOf(bucket.address).call())    

def currentPeriod() -> int:
    # blocktimestamp = 1630511586
    blocktimestamp = bucket.f.blockts().call()
    cliffTime = bucket.f.cliffTime().call()
    timeSinceCliff: int = blocktimestamp - cliffTime
    print(blocktimestamp)
    print(timeSinceCliff)
    
    # at cliff, one amount is withdrawable
    default_period = 1
    validPeriodCount: int = 1 + timeSinceCliff / default_period
    print("validPeriodCount ", validPeriodCount)
    # return validPeriodCount * claim.amountPeriod

    return validPeriodCount


if __name__=="__main__":

    a = accounts()
    tr = get_transactor(a)
    vtoken = token(a, tr)
    cta = deploy_bucket(tr, vtoken, a)
    # cta = deploy_bucket(tr, vtoken, a)
    # cta = "0x5c609Db3A64Fd1bD5d4dA467963090f88BE2574a"
    # cta = "0x2766EdFD8d91Bc23e3456C3AF9Cf74de4AebD956"
    bucket_ctr = tr.get_ctr("Bucket")
    bucket = tr.load_contract(cta, bucket_ctr.abi)

    txp = tr.get_tx_params(200000)
    tx = bucket.functions.initialize().buildTransaction(txp)
    signpush(tr, a[0], tx)

    print(bucket.functions.name().call())
    print("total claim ",bucket.f.totalClaimAmount().call())
    print("openClaimAmount  ",bucket.f.openClaimAmount().call())

    # deposittokens()

    txp = tr.get_tx_params(200000)
    # tx = bucket.f.addClaim(a[0].address, 100).buildTransaction(txp)
    # signpush(tr, a[0], tx)

    print(bucket.f.totalClaimAmount().call())
    print(bucket.f.openClaimAmount().call())
    print(bucket.f.totalWithdrawnAmount().call())

    print(bucket.f.getVestableAmount(a[0].address).call())

    # day = 86400*30
    # # increase_chaintime(day)

    # currentPeriod()

    # print("end time",bucket.f.endTime().call())
    # print("initialized",bucket.f.initialized().call())
    # print(bucket.f.getVestableAmount(a[0].address).call())
    
    # c = bucket.f.claims(a[0].address).call()
    # print("withdraw ", c[3])

    # txp = tr.get_tx_params(200000)
    # tx = bucket.f.vestClaimMax(a[0].address).buildTransaction(txp)
    # signpush(tr, a[0], tx)

    # txp = tr.get_tx_params(200000)
    # print(a[0].address)
    # txp = tr.get_tx_params(200000)
    # signpush(tr, a[0], tx)


    # cta = "0x5c609Db3A64Fd1bD5d4dA467963090f88BE2574a"
    # print("bucket at ", cta)
    # 
    # txp = tr.get_tx_params(200000)



    # print("balance ",vtoken.f.balanceOf(cta).call())
    # print(bucket.address)


    # last_height = tr.w3.eth.block_number
    # block = tr.w3.eth.get_block(last_height)
    # print(get_ts(block.timestamp))
    # increase_chaintime(day)

    # last_height = tr.w3.eth.block_number
    # block = tr.w3.eth.get_block(last_height)
    # print(get_ts(block.timestamp))
