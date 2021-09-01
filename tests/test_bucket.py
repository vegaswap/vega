#!/usr/bin/python3

import pytest
from brownie import chain

def test_basic(token, basicbucket, accounts):
    assert basicbucket.name() == "Somebucket"
    regtime = basicbucket.registerTime()
    assert regtime == chain.time()
    dur = basicbucket.duration()
    assert dur == 10
    cf = basicbucket.cliffTime()
    offset = cf - regtime
    assert basicbucket.endTime() == regtime + dur + offset



