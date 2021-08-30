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

from setup_tests import *

def test_issue(test_account, transactor, ntc):
    """ basic issuance """
    assert ntc.address[:2] == "0x"
    txp = transactor.get_tx_params(200000)
    tx = ntc.f.issue(test_account.address, 100).buildTransaction(txp)
    signpush(transactor, test_account, tx)
    v = ntc.f.balanceOf(test_account.address).call()
    assert v == 100

def test_reissue(test_account, transactor, ntc):
    """ cant issue second time """
    txp = transactor.get_tx_params(200000)
    tx = ntc.f.issue(test_account.address, 100).buildTransaction(txp)
    signpush(transactor, test_account, tx)

    try:
        txp = transactor.get_tx_params(200000)
        tx = ntc.f.issue(test_account.address, 100).buildTransaction(txp)
        assert False
    except:
        assert True


def test_redeem(test_account, transactor, ntc):
    """ cant issue second time """
    assert ntc.address[:2] == "0x"
    txp = transactor.get_tx_params(200000)
    tx = ntc.f.issue(test_account.address, 100).buildTransaction(txp)
    signpush(transactor, test_account, tx)
    v = ntc.f.balanceOf(test_account.address).call()
    assert v == 100

    txp = transactor.get_tx_params(200000)
    tx = ntc.f.redeem(test_account.address, 10).buildTransaction(txp)
    signpush(transactor, test_account, tx)
    v2 = ntc.f.balanceOf(test_account.address).call()
    assert v2 == 90

