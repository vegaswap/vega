# from brownie.contracts import NRT

from brownie.project.main import Project
import brownie.network.main as n
import os
from pathlib import Path

path = Path(os.getcwd())
print(type(path), path)
vega = Project("Vega", path)

# print (dir(vega))
# print (vega.VegaToken)
# print (vega.NRT)
print(vega.NRT.get_verification_info().keys())
# print (vega.NRT.get_verification_info()['flattened_source'])

addr = "0x0238cfac65135ea6f170abc64c4603afb19aaed7"

# import pdb
# pdb.set_trace()
# n.connect("bsctest")
n.connect("bscmain")

# print (self.networks)

nrt = vega.NRT.at(addr)
print(nrt)

# nrt.publish_source()

print(type(nrt))
print(dir(nrt))
print(nrt.__module__)
print(nrt.__class__)
# print (dict(nrt))
