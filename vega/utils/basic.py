# import brownie

# from brownie import (
#     VegaToken,
#     VestingMath,
#     VegaMaster,
#     VestingConstants,
#     VestingBucket,
#     accounts,
#     chain,
# )

import requests
from web3 import Web3
from web3.middleware import geth_poa_middleware
from eth_account import Account as EthAccount  # type: ignore
from eth_utils import to_bytes
from eth_abi import decode_abi
import json

URL = "https://127.0.0.1:8545"
w3 = Web3(Web3.HTTPProvider(URL))


def load_ctr():
    ctr = "VestingBucket"
    with open("./build/contracts/%s.json" % (ctr), "r") as f:
        return json.loads(f.read())


ctr = load_ctr()
abi = ctr["abi"]

# w3.eth.contract(address=address, abi=abi)
# print(abi.keys())

# vestingbucket.functions.vestClaimMax(a, {"from": a}).transact()

# master_address = "0x8ffce6B66218529E618C2182902182eE5167a9Bc"
# master = VegaMaster.at(master_address)
