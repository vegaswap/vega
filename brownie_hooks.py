from jinja2 import Template
import yaml
from pathlib import Path

def process():
    pass

predone = False
contractout = ''

def pre():
    global contractout
    with open('./brownie-config.yaml','r') as f:
        z = f.read()
    
    config = yaml.safe_load(z)    
    contractout = (config['project_structure']['contractout'])
    predone = True

def process(path, source):
    print("brownie_load_source ", path, " ", type(source))
    contractName = str(path.name).split(".")[0]

    # TODO
    # just insert contract name after contract line instead
    t = Template(source)

    debugfunctions = '''function errorMessage(string memory reason)
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
    }'''%(contractName, contractName)

    source = t.render(
        # header='string public constant contractName = "%s";' % contractName,
        debugfunctions=debugfunctions
    )

    fn = '%s/%s' % (contractout, path.name)
    print (fn)
    with open(fn, 'w') as f:
        f.write(source)

    # TODO generate flat file

    i = 0
    for line in source.split('\n'):
        print(i, ":", line)
        i += 1

    return source

def brownie_load_source(path, source):
    if not predone: pre()
    
    # print (prj)
    source = process(path, source)

    return source


   

    return source
