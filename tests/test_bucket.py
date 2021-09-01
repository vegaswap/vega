#!/usr/bin/python3

import pytest
from brownie import chain


def within(a, b):
    assert abs(a - b) < 5


def test_basic(token, basicbucket, accounts):
    assert basicbucket.name() == "Somebucket"
    regtime = basicbucket.registerTime()
    assert regtime == chain.time()
    dur = basicbucket.duration()
    assert dur == 10
    cf = basicbucket.cliffTime()
    offset = cf - regtime
    # assert basicbucket.endTime() == regtime + dur + offset
    within(basicbucket.endTime(), regtime + dur + offset)
