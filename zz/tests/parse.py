import re

def getl():
    with open("test_transferFrom.py","r") as f:
        ls = f.readlines()
        return ls

def match_balance():
    ls = getl()
    i = 0
    for l in ls:
        # pattern = '\s*token'
        pattern = 'token'
        # p = re.compile('*')
        # p = re.compile('[a-z]+')
        # p = re.compile('[\s]+[a-z]+')
        p1 = re.compile('(.+)(balanceOf)')
        p2 = re.compile('(.+)(balanceOf)(.+)call')
        # p = re.compile('([\s]+)(balanceOf)')
        # p = re.compile('[#]+')
        # result = re.match(pattern, l)
        result = p1.match(l)
        # print(result)
        if result:
            result = p2.match(l)
            if not result:
                print(i,l,end='')
        # print(l, end='')
        i+=1

def match_def():
    ls = getl()
    i = 0
    for l in ls:
        p1 = re.compile('(.+)(def)')
        p2 = re.compile('(.+)(def)(.+)transactor')
        result = p1.match(l)
        if result:
            result = p2.match(l)
            if not result:
                print(i,l,end='')
        # print(l, end='')
        i+=1        

match_def()
