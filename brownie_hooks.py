"""
contract preprocessing

"""
from jinja2 import Template
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


# def pre():
#     """set the out directory once at setup"""
#     global contractout
#     with open("./brownie-config.yaml", "r") as f:
#         z = f.read()

#     config = yaml.safe_load(z)
#     contractout = config["project_structure"]["contracts-post"]


def get_contract(w3, ctr):
    with open("./build/contracts/%s.json" % ctr, "r") as f:
        j = json.loads(f.read())
        contract = w3.eth.contract(abi=j["abi"], bytecode=j["bytecode"])
        return contract




def pre_hook():
    print(">>>>> START <<<<<<")
    # pre()
    # print("Name\tType")
    # deployedAddress = deploy_lib("Util")

    # handle libs
    # print ("deployedAddress ", deployedAddress)
    # deployedlibs["Util"] = deployedAddress
    # print (deployedlibs)

    # print (w3.eth.getBalance(mainaccount.address))


def post_hook():
    print(">>>>> DONE post_hook <<<<<<")
    print("processed %i solidity contracts" % solcount)
    print("processed %i vyper contracts" % vycount)



def get_content(fp):
    with open(fp, "r") as f:
        return f.read()




def count_import(lines):
    i = 0
    for line in lines:
        if "import" in line:
            i += 1

    return i



def sha1sum(filename):
    h = hashlib.sha1()
    b = bytearray(128 * 1024)
    mv = memoryview(b)
    with open(filename, "rb", buffering=0) as f:
        for n in iter(lambda: f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()


def process_source(path, source):
    global solcount, vycount
    contractName = str(path.name).split(".")[0]
    contractType = str(path.name).split(".")[1]
    # lines = source.split("\n")
    # # print ("lines ", len(lines))
    # ctrtype = contract_type(lines)
    # print("%s\t%s" % (path, source))
    # print("type ", contractEnd)
    if contractType == "sol":
        solcount += 1
    if contractType == "vy":
        vycount += 1

    # print (solcount, vycount)

    # source = replace_template(source, contractName)

    fn = "%s/%s" % (contractout, path.name)
    # filename = "path/to/file"
    print(fn)

    # os.chmod(fn, S_IWUSR|S_IREAD)
    # with open(fn, "w") as f:
    #     f.write(source)

    # read only file
    # os.chmod(fn, S_IREAD|S_IRGRP|S_IROTH)

    # if contractName == "NRT":
    #     gen_flatfile(contractName, source)

    # if contractName == "VegaToken":
    #     gen_flatfile(contractName, source)

    # hashsol = sha1sum("./contracts-post/VegaToken.sol")
    # hashabi = sha1sum("./contracts-post/VegaToken.abi")
    # hashbin = sha1sum("./contracts-post/VegaToken.bin")

    # with open("./contracts-post/contracts.md", "w") as f:
    #     # Vega contracts
    #     f.write("# Vega contracts\n\n")
    #     f.write("| File | sha1|\n")
    #     f.write("| :--: | :--:|\n")
    #     f.write("| VegaToken.sol | %s |\n" % hashsol)
    #     f.write("| VegaToken.abi | %s |\n" % hashabi)
    #     f.write("| VegaToken.bin | %s |\n" % hashbin)

    return source


def brownie_load_source(path, source):
    print("brownie_load_source")

    # print (prj)
    source = process_source(path, source)

    return source