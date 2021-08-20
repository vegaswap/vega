import json

def getj(ctr):
    fp = "./build/contracts/%s.json"%ctr
    with open(fp,"r") as f:
        return json.loads(f.read())

import hashlib

def sha256sum(filename):
    # h  = hashlib.sha256()
    h  = hashlib.sha1()
    b  = bytearray(128*1024)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        for n in iter(lambda : f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()


# j = getj("NRT")
# print (j.keys())
# # print (j["bytecode"])
# print (j["contractName"])
# print (j["bytecodeSha1"])


ctr = "NRT"
shasum = sha256sum("./contracts/%s.bin"%ctr)
print (shasum)


