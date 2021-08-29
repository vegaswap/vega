"""
contract preprocessing

"""
# from jinja2 import Template
import yaml
from pathlib import Path
from brownie import accounts
from web3 import Web3
import json
import os
from stat import S_IREAD, S_IRGRP, S_IROTH, S_IWUSR
import hashlib

contractout = ""
global solcount, vycount
solcount, vycount = 0, 0

deployedlibs = {}


def pre_hook():
    print(">>>>> START <<<<<<")
    print("Name\tType")

def post_hook():
    print(">>>>> DONE <<<<<<")
    print("processed %i solidity contracts" % solcount)
    print("processed %i vyper contracts" % vycount)



def get_content(fp):
    with open(fp, "r") as f:
        return f.read()


def process_source(path, source):
    global solcount, vycount
    contractName = str(path.name).split(".")[0]
    contractEnd = str(path.name).split(".")[1]
    lines = source.split("\n")
    # print("type ", contractEnd)
    if contractEnd == "sol":
        solcount += 1
    if contractEnd == "vy":
        vycount += 1

    return source


def brownie_load_source(path, source):
    # print("brownie_load_source")

    # print (prj)
    source = process_source(path, source)

    return source
