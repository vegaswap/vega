import sys

sys.path.insert(0, "/Users/ben/projects/vegaswap/repos/transactor")


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
import pytest

with open("./build/contracts/Bucket.json","r") as f:
    x = f.read()
    z = json.loads(x)
    print(z.keys())


# with open("vconfig.yaml") as f:
#     cfg = yaml.load(f, Loader=yaml.FullLoader)

# def signpush(transactor, account, tx):
#     signedtx = account.signTransaction(tx)
#     tx_receipt = transactor.pushtx(signedtx)
#     return tx_receipt

# def signpush_deploy(transactor, account, tx):
#     signedtx = account.signTransaction(tx)
#     tx_receipt = transactor.pushtx(signedtx)
#     return tx_receipt    

# def deploy(acct, transactor, ctr, pk):
#     dtx = transactor.get_deploy_tx(ctr, cargs=None)
#     tx_receipt = signpush_deploy(transactor, acct, dtx)
#     cta = tx_receipt["contractAddress"]
#     return cta

# def get_ctr(ctrname, accounts, pk1):
#     myaddr = accounts[0].address

#     transactor = transact.get_transactor("LOCAL", myaddr, cfg["builddir"], "")
    
#     ctr = transactor.get_ctr(ctrname)
#     print(ctr)
#     cta = deploy(accounts[0], transactor, ctr, pk1)
#     ctr = transactor.load_contract(cta, transactor.get_contract(ctrname).abi)
#     return ctr    

# pks = ["0x0fce4fd715a7a263cb127007cf8e685d1689e84ad8baa7a988ed3957f76a5d3a",
# "0x5d54c9926bc807d9b450190dd779cecd8da19ef60c040eb02e6a5a48f3d152d0",
# "0x3474a2dc495b0ae46b9ac1b81f67ec6a2acb3e9fe83634ad3f4caad1c43d0a76",
# "0x9cb670120feb5e70ae7218acf2c2c061958f9c7b47ee11afc9c9671a147683db",
# "0xce43593a1648024625db3d187098940d76786e39ce5563f9d0186e589219a860",
# "0xb291b4f245fc722e3958a3138b7bf5256ebc4c7c7998dafc4d9c82f899f3acc6",
# "0xf261312fe8819ac5a5bbda3432e9b228dc6b0c40ac8cc5d28c320fd6afe9c396",
# "0x3c6b3b0122ebf9717207a7a7a3da7b5899d07b6f9cd793fd29d15e4e41a6eceb",
# "0xbcf894fb1a3291a359f36244c2aaf80ea5db8a45faf7222f00fda576dcad0db8",
# "0xb7600ce592e8cb536869a8142d63e5460321885134fa184cc92e04fb45bdd1bb"]


# @pytest.fixture
# def accounts():
#     a = list()
#     for pk in pks:
#         accounta = Account()
#         acct = accounta.privateKeyToAccount(pk)
#         a.append(acct)
#     return a

# @pytest.fixture
# def transactor(accounts):
#     transactor = transact.get_transactor("LOCAL", accounts[0].address, cfg["builddir"], "")
#     return transactor

# @pytest.fixture
# def ntc(accounts, transactor):
#     myaddr = accounts[0].address

#     # with open("vconfig.yaml") as f:
#     #     cfg = yaml.load(f, Loader=yaml.FullLoader)

#     transactor = transact.get_transactor("LOCAL", myaddr, cfg["builddir"], "")
#     ctrname = "NTC"
#     ctr = transactor.get_ctr(ctrname)
#     print(ctr)
#     cta = deploy(accounts[0], transactor, ctr, pks[0])
#     ctr = transactor.load_contract(cta, transactor.get_contract(ctrname).abi)
#     return ctr

# @pytest.fixture
# def token(accounts, transactor):
#     myaddr = accounts[0].address

#     transactor = transact.get_transactor("LOCAL", myaddr, cfg["builddir"], "")
#     ctrname = "VegaToken"
#     ctr = transactor.get_ctr(ctrname)
#     cta = deploy(accounts[0], transactor, ctr, pks[0])
#     ctr = transactor.load_contract(cta, transactor.get_contract(ctrname).abi)
#     return ctr
