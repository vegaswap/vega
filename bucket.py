# import transact

# transactor = transact.get_transactor("BSC", ledger_account.address, cfg["builddir"], "")

"""
testing with private key on disk
"""
import sys

sys.path.insert(0, "/Users/ben/projects/vegaswap/repos/ledgertools")

from eth_account import Account
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

logger.add("account_tester.log", rotation="500 MB")
logger.add(
    sys.stdout, format="{time} {level} {message}", filter="my_module", level="INFO"
)

def signpush(transactor, account, tx, pk):
    signedtx = account.signTransaction(tx, pk)
    # log.info(signedtx)
    # transactor.activate_push()
    tx_receipt = transactor.pushtx(signedtx)
    # log.info(signedtx)
    return tx_receipt

def signpush_deploy(transactor, account, tx, pk):
    signedtx = account.signTransaction(tx, pk)
    # log.info(signedtx)
    # transactor.activate_push()
    tx_receipt = transactor.pushtx(signedtx)
    # log.info(signedtx)
    return tx_receipt    

def deploy(acct, transactor, nrt_contract):
    cargs = "VegaNRTPrv", "Vega NRT Private", "Private"
    dtx = transactor.get_deploy_tx(nrt_contract, cargs)
    tx_receipt = signpush_deploy(transactor, account, dtx)

    cta = tx_receipt["contractAddress"]
    print("deployed at ",cta)

def dump_ctr(newctrmap):
    ctrmap = load_ctr()
    print (newctrmap)
    for k,v in newctrmap.items():
        ctrmap[k]=v
    with open("contracts_local.json","w") as f:
        f.write(json.dumps(ctrmap))

def load_ctr():
    with open("contracts_local.json","r") as f:
        return json.loads(f.read())

def deploy_token(account, transactor, pk):
    contract_name = "VegaToken"
    vega_contract = transactor.get_contract(contract_name)
    # cta = "0x6FF692602b4aD0BC65fd67dFD5bD93FCFbd8E621"
    # nrt = transactor.load_contract(cta, nrt_contract.abi)
    dtx = transactor.get_deploy_tx(vega_contract)
    tx_receipt = signpush_deploy(transactor, account, dtx, pk)

    cta = tx_receipt["contractAddress"]
    print("deployed at ",cta)
    ctrmap = dict()
    ctrmap[contract_name] = cta
    dump_ctr(ctrmap)

def deploy_bucket(account, transactor, pk):
    contract_name = "VestingBucket"
    bucket_contract = transactor.get_contract(contract_name)

    # VegaToken = Web3.toChecksumAddress("0xc8F07C573fd0dD24382621afa8D69829AeCd77d8")

    # cta = "0x6FF692602b4aD0BC65fd67dFD5bD93FCFbd8E621"
    # nrt = transactor.load_contract(cta, nrt_contract.abi)
    import time
    cliff = int(time.time()+1)
    cargs = VegaToken.address, cliff, 10, 1000
    print(cargs)
    print (">> ",type(VegaToken.address))
    dtx = transactor.get_deploy_tx(bucket_contract, cargs)
    tx_receipt = signpush_deploy(transactor, account, dtx, pk)

    cta = tx_receipt["contractAddress"]
    print("deployed at ",cta)
    ctrmap = dict()
    ctrmap[contract_name] = cta
    dump_ctr(ctrmap)    
    

# def deploy_bucket(acct, transactor, nrt_contract):
#     # cliff = chain.time() + 100
#     # total = 1000
#     # period = 1
#     # vestingbucket = VestingBucket.deploy(
#     #     token, cliff, period, total, {"from": accounts[0]}
#     # )
#     dtx = transactor.get_deploy_tx(nrt_contract, cargs)
#     tx_receipt = signpush_deploy(transactor, account, dtx)

#     cta = tx_receipt["contractAddress"]
#     print("deployed at ",cta)    

def issue_redeem(transactor):
    contract_name = "NRT"
    nrt_contract = transactor.get_contract(contract_name)
    cta = "0x6FF692602b4aD0BC65fd67dFD5bD93FCFbd8E621"
    nrt = transactor.load_contract(cta, nrt_contract.abi)

    # signpush(transactor, account, tx)

    # with open("contracts.json", "r") as f:
    #     ctrmap = json.loads(f.read())

    # NRTaddress = ctrmap["NRTPrivate"]
    # NRTprivaddress = ctrmap["NRTPrivate"]

    # gas = 44751
    # gas = 61422
    gas = 100000
    txp = transactor.get_tx_params(gas)
    # tx = nrt.functions.issue(acct2.address, 100).buildTransaction(txp)
    # print (tx)

    tx = nrt.functions.redeem(acct2.address, 100).buildTransaction(txp)
    print (tx)

    signpush(transactor, account, tx, pk)
    print (">> ", nrt.functions.issuedSupply().call())
    print (">> ", nrt.functions.totalSupply().call())


if __name__ == "__main__":

    # home = str(Path.home())
    # f = "bsc_mainnet.toml"
    # p = Path(home, ".chaindev", f)
    # secrets = toml.load(p)
    # pk = secrets["PRIVATEKEY"]
    # print(pk)
    pk = "0x24cbbcbac2ae33cb88f8b75cfbbd6953dd72c6a8588a163e2d64aca14219332a"
    pk2 = "0x5aa9dc03c05e729251e20f3c88b28202a0e966bb676e2a43b36998b3f4703bd2"

    account = Account()
    acct = account.privateKeyToAccount(pk)
    myaddr = acct.address
    print(myaddr)

    account2 = Account()
    acct2 = account2.privateKeyToAccount(pk2)

    with open("config.yaml") as f:
        cfg = yaml.load(f, Loader=yaml.FullLoader)

    transactor = transact.get_transactor("LOCAL", myaddr, cfg["builddir"], "")
    print(transactor)

    #brownie like magic insert into global namespace
    cmap = load_ctr()
    print (cmap)
    ctrname = "VegaToken"
    ctr = transactor.get_contract(ctrname)
    cta = cmap[ctrname]
    ctr = transactor.load_contract(cta, ctr.abi)

    globals()[ctrname] = ctr
    print (VegaToken.functions.totalSupply().call())
    print (VegaToken.address)

    # deploy_bucket(account, transactor, pk)

    bucketaddr = "0x6750B5774E2BB63d1A6556eE36AAE95bc10B197b"
    ctrname = "VestingBucket"
    ctr = transactor.get_contract(ctrname)
    cta = cmap[ctrname]
    bucket = transactor.load_contract(bucketaddr, ctr.abi)
    # print(bucket.functions.depositOwner(100).call())
    print(bucket.functions.depositOwner(100).call())

    # globals()[ctrname] = ctr
    # print (VegaToken.functions.totalSupply().call())
    # print (VegaToken.address)


    
    # deploy_token(account, transactor, pk)

    

    # contract_name = "NRT"
    # nrt_contract = transactor.get_contract(contract_name)
    # cta = "0x6FF692602b4aD0BC65fd67dFD5bD93FCFbd8E621"
    # nrt = transactor.load_contract(cta, nrt_contract.abi)
    

    # deploy(acct, transactor, nrt_contract)

    

