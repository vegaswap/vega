#!/usr/bin/python3

from brownie import VegaToken, VestingMath, VegaMaster, VestingBucket, accounts

import time


def get_invfile():
    with open("invdb.csv", "r") as f:
        lines = f.readlines()
    return lines


def get_inv():
    lines = get_invfile()
    start = 3
    claims = list()
    for line in lines[start:]:
        line = line.replace("\n", "")
        arr = line.split(",")
        amount, addr = int(arr[0]), arr[1]
        claims.append([addr, amount])

    return claims


def main():
    # get private claims
    claims = get_inv()
    for claim in claims:
        print(claim)
