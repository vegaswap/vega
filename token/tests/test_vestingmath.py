#!/usr/bin/python3
import brownie

from brownie import chain, VestingMath, accounts
import time

days = 60*60*24
days30 = days*30


def test_basic(accounts, vestingmath, token):
    a = accounts[0]

    assert vestingmath.ceildiv(2, 1) == 2

    assert vestingmath.ceildiv(2, 1) == 2
    assert vestingmath.ceildiv(6, 2) == 3
    assert vestingmath.ceildiv(99, 3) == 33
    assert vestingmath.ceildiv(11, 2) == 6
    assert vestingmath.ceildiv(44, 33) == 2

    assert vestingmath.DEFAULT_PERIOD() == days30

    #t1 = int(time.time() + 5 * days)
    #assert controller.getEndTime(t1, 10, 100) == t1 * 10 * days30
    assert vestingmath.getEndTime(0, 10, 100) == 10 * days30

    t1 = int(time.time())
    assert vestingmath.getEndTime(t1, 10, 100) == t1 + 10 * days30


def test_vest(vestingmath):
    blocktime = 1001
    cliff = 900
    endtime = 3000
    amountPerPeriod = 10
    total = 200
    period = 100
    amount = vestingmath.getVestedAmountTSX(
        blocktime, cliff, endtime, amountPerPeriod, total, period)
    assert amount == 20

    blocktime = 999
    cliff = 900
    endtime = 3000
    period = 100
    amountPerTerminalPeriod = 10
    total = 200
    amount = vestingmath.getVestedAmountTSX(
        blocktime, cliff, endtime, amountPerTerminalPeriod, total, period)
    assert amount == 10

    blocktime = 800
    cliff = 900
    endtime = 3000
    period = 100
    amountPerTerminalPeriod = 10
    total = 200
    amount = vestingmath.getVestedAmountTSX(
        blocktime, cliff, endtime, amountPerTerminalPeriod, total, period)
    assert amount == 0

    blocktime = 1010
    cliff = 900
    endtime = 3000
    period = 100
    amountPerTerminalPeriod = 13
    total = 200
    amount = vestingmath.getVestedAmountTSX(
        blocktime, cliff, endtime, amountPerTerminalPeriod, total, period)
    assert amount == 26

    blocktime = 2900
    cliff = 900
    endtime = 3000
    period = 100
    amountPerTerminalPeriod = 13
    total = 200
    amount = vestingmath.getVestedAmountTSX(
        blocktime, cliff, endtime, amountPerTerminalPeriod, total, period)
    assert amount == 200
