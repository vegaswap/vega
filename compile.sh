#!/bin/bash
sudo rm build/*.*
cd contracts-vy
vyper NTC.vy -f abi > ../build/NTC.abi
vyper NTC.vy -f bytecode > ../build/NTC.bin

# vyper Bucket.vy -f abi > ../build/Bucket.abi
# vyper Bucket.vy -f bytecode > ../build/Bucket.bin

# vyper VegaToken.vy -f abi > ../build/VegaToken.abi
# vyper VegaToken.vy -f bytecode > ../build/VegaToken.bin%