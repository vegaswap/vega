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

contractout = ''
global solcount, vycount
solcount, vycount = 0,0

deployedlibs = {}

def pre():
    """ set the out directory once at setup """
    global contractout
    with open("./brownie-config.yaml", "r") as f:
        z = f.read()

    config = yaml.safe_load(z)
    contractout = config["project_structure"]["contractout"]

def get_contract(w3, ctr):
    with open("./build/contracts/%s.json"%ctr,"r") as f:
        j = json.loads(f.read())
        contract = w3.eth.contract(abi=j["abi"], bytecode=j["bytecode"])
        return contract

def deploy_lib(contractName):
    accounts.load("vegabsctest")
    mainaccount = accounts[0]
   
    URL = "http://localhost:8545"
    w3 = Web3(Web3.HTTPProvider(URL))
    ctr = get_contract(w3, contractName)

    nonce = w3.eth.getTransactionCount(mainaccount.address)

    # estgas = w3.eth.estimate_gas({'from': mainaccount.address})

    txparams = {
                'from': mainaccount.address,
                # 'to': '',
                "nonce": nonce,
                "gas": 660000,
                "gasPrice": w3.toWei('5', 'gwei')}

    # txparams["gas"] = estgas

    tx = ctr.constructor().buildTransaction(txparams)

    signedtx = w3.eth.account.signTransaction(tx, pk)
    result = w3.eth.sendRawTransaction(signedtx.rawTransaction)
    rh = result.hex()

    tx_receipt = w3.eth.waitForTransactionReceipt(rh)
    # print(tx_receipt['status'])
    # print(tx_receipt['blockNumber'])
    deployedAddress = tx_receipt.contractAddress
    print("gasUsed ",tx_receipt['gasUsed'])
    return deployedAddress

def pre_hook():
    print (">>>>> START <<<<<<")
    pre()
    print("Name\tType")
    # deployedAddress = deploy_lib("Util")

    # handle libs
    # print ("deployedAddress ", deployedAddress)
    # deployedlibs["Util"] = deployedAddress
    # print (deployedlibs)

    # print (w3.eth.getBalance(mainaccount.address))

def post_hook():
    print (">>>>> DONE <<<<<<")
    print ("processed %i solidity contracts"%solcount)
    print ("processed %i vyper contracts"%vycount)
    

def contract_type(lines):
    for line in lines:
        if line == "": continue
        if line.startswith("//"): continue
        if line.startswith("import"): continue
        if line.startswith("pragma"): continue

        if line.startswith("contract"): return "contract"
        if line.startswith("abstract contract"): return "abstractcontract"
        if line.startswith("library"): return "library"
        if line.startswith("interface"): return "interface"

    return "Error"

def iscontract(lines):
    #find the definition line
    pass
    

    # for line in lines:
    #     if line.startsWith("contract"):
    #         return True
    #     if line.startsWith("abstract contract"):
    #         return False
    #     if line.startWith("library"):
    #         return False
    #     if line.startsWith("interface"):
    #         return False

def replace_template(source, contractName):
# TODO
    # just insert contract name after contract line instead
    t = Template(source)

    # util_address = "0x0c11645843Ea5edC413efB304692d8Ccb06ED4D2"
    #TESTNET
    util_address = deployedlibs["Util"]
    print (">>>>>>> ", util_address)
    # util_address = "0xa3B53dDCd2E3fC28e8E130288F2aBD8d5EE37472"

    debugfunctions = """IUtil constant util =
        IUtil(%s);
        
    function errorMessage(string memory reason)
        private
        pure
        returns (string memory)
    {
        return util.errorMessage("%s", reason);
    }

    function errorMessage(string memory reason, string memory data)
        private
        pure
        returns (string memory)
    {
        return util.errorMessage("%s", reason, data);
    }""" % (
        util_address,
        contractName,
        contractName,
    )

    # if ctr == "contract" or ctr == "abstractcontract":
    #     print ('>> ',lines[-2:])
    #     newlines = lines[:-2] + ['\n'] + debugfunctions.split('\n') + ['\n}']
    #     source = '\n'.join(newlines)
    # elif ctr == "library":
    #     print ("library. dont add error handling")
    # elif ctr == "abstractcontract":
    #     print ("abstractcontract. dont add error handling")
    # elif ctr == "interface":
    #     print ("interface. dont add error handling")

    source = t.render(
        # header='string public constant contractName = "%s";' % contractName,
        debugfunctions=debugfunctions
    )    
    return source

def process_source(path, source):
    global solcount, vycount
    contractName = str(path.name).split(".")[0]
    contractEnd = str(path.name).split(".")[1]
    lines = source.split('\n')
    # print ("lines ", len(lines))
    ctrtype = contract_type(lines)
    print("%s\t%s"%(contractName,ctrtype))
    # print("type ", contractEnd)
    if contractEnd == "sol":
        solcount+=1
    if contractEnd == "vy":
        vycount+=1

    # print (solcount, vycount)

    # source = replace_template(source, contractName)    

    
    fn = "%s/%s" % (contractout, path.name)
    # filename = "path/to/file"
    # print(fn)
    

    # os.chmod(fn, S_IWUSR|S_IREAD)
    with open(fn, "w") as f:
        f.write(source)

    # read only file
    # os.chmod(fn, S_IREAD|S_IRGRP|S_IROTH)

    # TODO generate flat file
    # i = 0
    # for line in source.split('\n'):
    #     print(i, ":", line)
    #     i += 1

    return source


def brownie_load_source(path, source):
    # print("brownie_load_source")

    # print (prj)
    source = process_source(path, source)

    return source
