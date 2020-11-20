#remove files
rm -rf ./-p/
rm -rf /tmp/ethbuild

#!/bin/bash
mkdir /tmp/ethbuild -p && solc --bin --abi Model.sol -o /tmp/ethbuild/ --overwrite && abigen --bin=/tmp/ethbuild/Model.bin --abi=/tmp/ethbuild/Model.abi --pkg=contract --out=Model.go