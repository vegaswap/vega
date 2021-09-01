#!/bin/bash
sudo rm build/*.*
cd contracts-vy

vyper Bucket.vy -f abi > ../build/Bucket.abi
vyper Bucket.vy -f bytecode > ../build/Bucket.bin

vyper VegaToken.vy -f abi > ../build/VegaToken.abi
vyper VegaToken.vy -f bytecode > ../build/VegaToken.bin

vyper Claimlist.vy -f abi > ../build/Claimlist.abi
vyper Claimlist.vy -f bytecode > ../build/Claimlist.bin