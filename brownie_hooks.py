"""
contract preprocessing

"""
from jinja2 import Template
import yaml
from pathlib import Path


predone = False
contractout = ""

def pre():
    """ set the out directory once at setup """
    global predone
    global contractout
    with open("./brownie-config.yaml", "r") as f:
        z = f.read()

    config = yaml.safe_load(z)
    contractout = config["project_structure"]["contractout"]
    predone = True

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

def process_source(path, source):
    contractName = str(path.name).split(".")[0]

    lines = source.split('\n')
    print ("lines ", len(lines))

    ctr = contract_type(lines)
    print (">> ", ctr)
    

    # TODO
    # just insert contract name after contract line instead
    t = Template(source)

    debugfunctions = """    function errorMessage(string memory reason)
        private
        pure
        returns (string memory)
    {
        return Util.errorMessage("%s", reason);
    }

    function errorMessage(string memory reason, string memory data)
        private
        pure
        returns (string memory)
    {
        return Util.errorMessage("%s", reason, data);
    }""" % (
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

    fn = "%s/%s" % (contractout, path.name)
    print(fn)
    with open(fn, "w") as f:
        f.write(source)

    # TODO generate flat file
    # i = 0
    # for line in source.split('\n'):
    #     print(i, ":", line)
    #     i += 1

    return source


def brownie_load_source(path, source):
    print("brownie_load_source ", path)
    if not predone:
        pre()

    # print (prj)
    source = process_source(path, source)

    return source
