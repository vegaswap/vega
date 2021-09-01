#!/usr/bin/python3

import pytest


def test_add(xlist, accounts):
    assert xlist.count() == 0
    xlist.addItem(accounts[0], 100)
    assert xlist.count() == 1


def test_addget(xlist, accounts):
    assert xlist.count() == 0
    xlist.addItem(accounts[0], 100)
    assert xlist.getAmount(0).return_value == 100
    assert xlist.getAddress(0).return_value == accounts[0]
    assert xlist.count() == 1
