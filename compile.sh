#!/bin/bash
sudo rm build/*.*
cd contracts-vy

vyper Bucket.vy -f abi > ../build/Bucket.abi
vyper Bucket.vy -f bytecode > ../build/Bucket.bin

vyper VegaToken.vy -f abi > ../build/VegaToken.abi
vyper VegaToken.vy -f bytecode > ../build/VegaToken.bin

vyper Xlist.vy -f abi > ../build/Xlist.abi
vyper Xlist.vy -f bytecode > ../build/Xlist.bin