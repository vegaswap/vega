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
            info.extend([f,s])
    # build_files[tok(f)] = s
    return info

# xe = edn.dumps(build_files)

def write_table(mdFile, data):
    col = 2
    x = int(len(data)/col)
    print (x)
    # mdFile.new_table(columns=2, rows=x, text=data, text_align='center')
    mdFile.new_table(columns=2, rows=x, text=data, text_align='center')


mdFile = MdUtils(file_name='ContractBuild',title='Vega Contract Build Info')
mdFile.new_header(level=1, title='Contracts')
mdFile.new_paragraph("Vega Contract information")
# list_of_strings = ["Items", "Data"]
# r = 1
# c = 2
# for x in range(5):
#     list_of_strings.extend(["Item", str(x)])
#     r+=1

info = ["File", "sha1hash"]
info += get_info(".bin")
info += get_info(".abi")
mdFile.new_line()
# print (c,r)
write_table(mdFile, info)

mdFile.create_md_file()


