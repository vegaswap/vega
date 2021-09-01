#!/bin/bash
sudo rm build/*.*
cd contracts-vy

 vyper -o ../build Bucket.vy -f abi
 vyper -o ../build Bucket.vy -f bytecode
 vyper -o ../build VegaToken.vy -f abi
 vyper -o ../build VegaToken.vy -f bytecode
 vyper -o ../build Xlist.vy -f abi
 vyper -o ../build Xlist.vy -f bytecode