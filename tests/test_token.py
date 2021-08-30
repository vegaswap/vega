# import sys

# sys.path.insert(0, "/Users/ben/projects/vegaswap/repos/transactor")

# from eth_account import Account
# from web3 import Web3
# import toml
# from pathlib import Path

# from web3.types import SignedTx
# import transact
# from loguru import logger
# import sys
# import toml
# import yaml
# import json
# import pytest

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

# @pytest.fixture
# def pk1():
#     pk = "0x0fce4fd715a7a263cb127007cf8e685d1689e84ad8baa7a988ed3957f76a5d3a"
#     return pk

# @pytest.fixture
# def pk2():
#     pk = "0x5d54c9926bc807d9b450190dd779cecd8da19ef60c040eb02e6a5a48f3d152d0"
#     return pk

# @pytest.fixture
# def test_account(pk1):
#     accounta = Account()
#     acct = accounta.privateKeyToAccount(pk1)
#     return acct

# @pytest.fixture
# def test_account2(pk2):
#     accounta = Account()
#     acct = accounta.privateKeyToAccount(pk2)
#     return acct    

# @pytest.fixture
# def transactor(test_account):
    
#     transactor = transact.get_transactor("LOCAL", test_account.address, cfg["builddir"], "")
#     return transactor

# @pytest.fixture
# def token(test_account, pk1):
#     myaddr = test_account.address

#     # with open("vconfig.yaml") as f:
#     #     cfg = yaml.load(f, Loader=yaml.FullLoader)

#     transactor = transact.get_transactor("LOCAL", myaddr, cfg["builddir"], "")
#     ctrname = "VegaToken"
#     ctr = transactor.get_ctr(ctrname)
#     cta = deploy(test_account, transactor, ctr, pk1)
#     ctr = transactor.load_contract(cta, transactor.get_contract(ctrname).abi)
#     return ctr


# def test_basic(test_account, test_account2, transactor, token, mypk):
#     """ balance is 0 """
#     #seonc account

#     token.approve(test_account2, 10 ** 19, {"from": test_account})
#     assert token.allowance(test_account, test_account2) == 10 ** 19




