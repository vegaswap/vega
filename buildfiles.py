import os

wdir = "./build"
ld = os.listdir(wdir)
import hashlib
import edn_format as edn

tok = edn.Keyword


def sha1sum(filename):
    h = hashlib.sha1()
    b = bytearray(128 * 1024)
    mv = memoryview(b)
    with open(filename, "rb", buffering=0) as f:
        for n in iter(lambda: f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()


from mdutils.mdutils import MdUtils


def get_info(ext):
    info = []
    for f in ld:
        fp = os.path.join(wdir, f)
        if f.endswith(ext):
            s = sha1sum(fp)
            info.extend([f, s])
    # build_files[tok(f)] = s
    return info


import json


def get_contracts():
    with open("contracts.json", "r") as f:
        x = f.read()
    return json.loads(x)


cmap = get_contracts()
print(cmap)

clist = ["Contract", "address"]
for k in cmap.keys():
    clist.extend([k, cmap[k]])
    # print (str(k),cmap[k])

print(clist)
# cmap[tok("NRT")]


def write_table(mdFile, data):
    col = 2
    x = int(len(data) / col)
    # mdFile.new_table(columns=2, rows=x, text=data, text_align='center')
    mdFile.new_table(columns=2, rows=x, text=data, text_align="center")


mdFile = MdUtils(file_name="ContractBuild", title="Vega Contracts")
mdFile.new_header(level=1, title="Contract files")
mdFile.new_paragraph("Vega Contract file information")


info = ["File", "sha1hash"]
info += get_info(".bin")
info += get_info(".abi")
mdFile.new_line()
# print (c,r)
write_table(mdFile, info)

mdFile.new_header(level=1, title="Vega smart contracts")
mdFile.new_paragraph("Vega Contract chain information")

write_table(mdFile, clist)

mdFile.create_md_file()
