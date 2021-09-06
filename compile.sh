#!/bin/bash
sudo rm build/*.*
cd contracts-vy

vyper Bucket.vy -o ../build/Bucket.abi -f abi
vyper Bucket.vy -o ../build/Bucket.bin -f bytecode

vyper VegaToken.vy -o ../build/VegaToken.abi -f abi
vyper VegaToken.vy -o ../build/VegaToken.bin -f bytecode

vyper Claimlist.vy -o ../build/Claimlist.abi -f abi
vyper Claimlist.vy -o ../build/Claimlist.bin -f bytecode
