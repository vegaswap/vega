#!/usr/bin/python3
import brownie

from brownie import chain, VestingMath, accounts
import time

days = 60 * 60 * 24
days30 = days * 30


def test_basic(accounts, vestingmath, token):
    a = accounts[0]

    assert vestingmath.ceildiv(2, 1) == 2

    assert vestingmath.ceildiv(2, 1) == 2
    assert vestingmath.ceildiv(6, 2) == 3
    assert vestingmath.ceildiv(99, 3) == 33
    assert vestingmath.ceildiv(11, 2) == 6
    assert vestingmath.ceildiv(44, 33) == 2

    assert vestingmath.DEFAULT_PERIOD() == days30

    # t1 = int(time.time() + 5 * days)
    # assert controller.getEndTime(t1, 10, 100) == t1 * 10 * days30
    assert vestingmath.getEndTime(0, 10, 100) == 10 * days30

    t1 = int(time.time())
    assert vestingmath.getEndTime(t1, 10, 100) == t1 + 10 * days30


def test_vest(vestingmath):

    period = vestingmath.DEFAULT_PERIOD()
    assert period == 60 * 60 * 24 * 30

    blocktime = 1001
    cliff = 900
    # endtime = 3000
    endtime = blocktime + 20 * period
    amountPerPeriod = 10
    total = 200
    amount = vestingmath.getVestedAmount(
        blocktime, cliff, endtime, amountPerPeriod, total
    )
    assert amount == amountPerPeriod

    blocktime = endtime
    amount = vestingmath.getVestedAmount(
        blocktime, cliff, endtime, amountPerPeriod, total
    )
    assert amount == total

    blocktime = 999
    cliff = 900
    endtime = 3000
    amountPerTerminalPeriod = 10
    total = 200
    amount = vestingmath.getVestedAmount(
        blocktime, cliff, endtime, amountPerTerminalPeriod, total
    )
    assert amount == amountPerTerminalPeriod

    blocktime = 800
    cliff = 900
    endtime = 3000
    amountPerTerminalPeriod = 10
    total = 200
    amount = vestingmath.getVestedAmount(
        blocktime, cliff, endtime, amountPerTerminalPeriod, total
    )
    assert amount == 0

    blocktime = 901
    cliff = 900
    endtime = 3000
    amountPerTerminalPeriod = 10
    total = 200
    amount = vestingmath.getVestedAmount(
        blocktime, cliff, endtime, amountPerTerminalPeriod, total
    )
    assert amount == 10

    cliff = 900
    blocktime = cliff + 20 * period
    endtime = 3000
    amountPerTerminalPeriod = 10
    total = 200
    amount = vestingmath.getVestedAmount(
        blocktime, cliff, endtime, amountPerTerminalPeriod, total
    )
    assert amount == total

    cliff = 900
    blocktime = cliff + 20 * period
    endtime = 3000
    amountPerTerminalPeriod = 13
    total = 200
    amount = vestingmath.getVestedAmount(
        blocktime, cliff, endtime, amountPerTerminalPeriod, total
    )
    assert amount == total

    cliff = 900
    period = 60 * 60 * 24 * 30
    endtime = cliff + 20 * period
    amountPerPeriod = 13
    total = 200
    from vestingmath import getVestedAmount

    # assert period ==

    for n in range(0, 14):
        blocktime = cliff + n * period
        v = getVestedAmount(blocktime, cliff, endtime, amountPerPeriod, total, period)
        assert v == amountPerTerminalPeriod * (n + 1)

    n = 15
    blocktime = cliff + n * period
    v = getVestedAmount(blocktime, cliff, endtime, amountPerPeriod, total, period)
    assert v == 200

    ######

    for n in range(0, 14):
        blocktime = cliff + n * period
        v = vestingmath.getVestedAmount(
            blocktime, cliff, endtime, amountPerTerminalPeriod, total
        )
        assert v == amountPerTerminalPeriod * (n + 1)

    n = 15
    blocktime = cliff + n * period
    v = vestingmath.getVestedAmount(
        blocktime, cliff, endtime, amountPerTerminalPeriod, total
    )
    assert v == 200

    # cliff = 900
    # blocktime = cliff + 2 * period
    # endtime = 3000
    # amountPerTerminalPeriod = 13
    # total = 200
    # amount = vestingmath.getVestedAmount(
    #     blocktime, cliff, endtime, amountPerTerminalPeriod, total
    # )
    # assert amount == 2 * amountPerTerminalPeriod

    # blocktime = 2900
    # cliff = 900
    # endtime = 3000
    # amountPerTerminalPeriod = 13
    # total = 200
    # amount = vestingmath.getVestedAmount(
    #     blocktime, cliff, endtime, amountPerTerminalPeriod, total
    # )
    # assert amount == 200
