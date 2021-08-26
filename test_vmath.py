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

import bucket

def deploy_vmath(account, transactor, pk):
    contract_name = "Vestingmath"
    vega_contract = transactor.get_contract(contract_name)
    # cta = "0x6FF692602b4aD0BC65fd67dFD5bD93FCFbd8E621"
    # nrt = transactor.load_contract(cta, nrt_contract.abi)
    dtx = transactor.get_deploy_tx(vega_contract)
    tx_receipt = signpush_deploy(transactor, account, dtx, pk)

    cta = tx_receipt["contractAddress"]
    print("deployed at ",cta)
    ctrmap = dict()
    ctrmap[contract_name] = cta
    bucket.dump_ctr(ctrmap)
    

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
    cmap = bucket.load_ctr()
    print (cmap)
    ctrname = "VegaToken"
    ctr = transactor.get_contract(ctrname)
    cta = cmap[ctrname]
    ctr = transactor.load_contract(cta, ctr.abi)

    globals()[ctrname] = ctr
    print (VegaToken.functions.totalSupply().call())
    print (VegaToken.address)


    ctrname = "Vestingmath"
    cta = cmap[ctrname]

    # ctrname = "VestingBucket"
    # ctr = transactor.get_contract(ctrname)

    # deploy_vmath(account, transactor, pk)

    
    abi = transactor.load_abi(ctrname)
    print (abi)
    ctr = transactor.load_contract(cta, abi)
    globals()[ctrname] = ctr
    # print (VegaToken.functions.totalSupply().call())
    # print (VegaToken.address)

    print (">> ",Vestingmath.address)

    print (dir(Vestingmath))
    # print (Vestingmath.functions.days)
    _cliffTime = 0
    _amountPerPeriod = 10
    _totalAmount = 100
    v = Vestingmath.functions.getEndTime(_cliffTime, _amountPerPeriod, _totalAmount).call()
    # print(v)

    import time
    days = 2592000
    nowt = int(time.time())
    blocktime = nowt
    cliffTime = nowt
    endTime = nowt + 300*days
    amountPerPeriod = 10
    totalAmount = 100

    timeSinceCliff = blocktime - cliffTime

    v = Vestingmath.functions.getVestedAmountPeriod(blocktime, cliffTime, endTime, amountPerPeriod, totalAmount).call()
    print("amount ",v)

    import vestingmath
    DEFAULT_PERIOD = 30 * days
    period = DEFAULT_PERIOD
    blocktime += DEFAULT_PERIOD
    x = vestingmath.getVestedAmountPeriod(blocktime, cliffTime, endTime, amountPerPeriod, totalAmount)
    print("next ",x)


    # deploy_token(account, transactor, pk)

    

    # contract_name = "NRT"
    # nrt_contract = transactor.get_contract(contract_name)
    # cta = "0x6FF692602b4aD0BC65fd67dFD5bD93FCFbd8E621"
    # nrt = transactor.load_contract(cta, nrt_contract.abi)
    

    # deploy(acct, transactor, nrt_contract)

    

