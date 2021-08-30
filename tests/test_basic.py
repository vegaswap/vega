from setup_tests import *

def test_basic(accounts, transactor, token, pk1):
    """ balance is 0 """
    assert token.address[:2] == "0x"    
    v = token.f.balanceOf(accounts[0].address).call()
    assert v == 10**9 * 10**18

    v = token.f.balanceOf(accounts[1].address).call()
    assert v == 0
