# import brownie.network.contract as c
import json
import hashlib

def sha1sum(filename):
    h = hashlib.sha1()
    b = bytearray(128 * 1024)
    mv = memoryview(b)
    with open(filename, "rb", buffering=0) as f:
        for n in iter(lambda: f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()

def write_buid(ctr):
    with open("brownie-build/contracts/%s.json"%ctr,"r") as f:
        x = json.loads(f.read())
        bt = x["bytecode"]
        hs = hashlib.sha1(bt.encode('utf-8')).hexdigest()
        fp = "./build/%s.bin"%ctr
        print(fp,hs)
        with open(fp,"w") as f:
            f.write(bt)

        bt = x["abi"]
        hs = hashlib.sha1(str(bt).encode('utf-8')).hexdigest()
        fp = "./build/%s.abi"%ctr
        print(fp,hs)
        with open(fp,"w") as f:
            f.write(str(bt))

ctr = "Bucket"
write_buid(ctr)
ctr = "VegaToken"
write_buid(ctr)
ctr = "ClaimList"
write_buid(ctr)