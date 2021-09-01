from setup_tests import *

# def test_basic(accounts, transactor, pk1):
#     """ balance is 0 """
#     # ta = test_account(pk1())
#     myaddr = test_account.address
#     transactor = transact.get_transactor("LOCAL", myaddr, cfg["builddir"], "")
    
#     xlist_ctr = get_ctr("XList",test_account, pk1)
#     v = xlist_ctr.f.count().call()

#     txp = transactor.get_tx_params(200000)
#     tx = xlist_ctr.f.addItem(myaddr, 1000).buildTransaction(txp)
#     signpush(transactor, test_account, tx)

#     v1 = xlist_ctr.f.count().call()
#     assert v1 == 1
