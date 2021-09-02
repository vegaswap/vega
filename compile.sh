#!/bin/bash
sudo rm build/*.*
cd contracts-vy

vyper Bucket.vy -o ../build -f abi
vyper Bucket.vy -o ../build -f bytecode

vyper VegaToken.vy -o ../build -f abi
vyper VegaToken.vy -o ../build -f bytecode

vyper Claimlist.vy -o ../build -f abi
vyper Claimlist.vy -o ../build -f bytecode
