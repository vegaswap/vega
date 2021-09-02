import hashlib

def sha1sum(filename):
    h = hashlib.sha1()
    b = bytearray(128 * 1024)
    mv = memoryview(b)
    with open(filename, "rb", buffering=0) as f:
        for n in iter(lambda: f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()


def show_hash(f):
    hashx = sha1sum(f)
    print(f, hashx)

# hashvy = sha1sum("./contracts-vy/VegaToken.vy")
# hashabi = sha1sum("./build/VegaToken.abi")
# hashbin = sha1sum("./build/VegaToken.bin")

for ctr in ["VegaToken", "Bucket", "ClaimList"]:
    f = ["./contracts-vy/%s.vy"%ctr, "./build/%s.abi"%ctr, "./build/%s.bin"%ctr]
    for x in f:
        show_hash(x)
