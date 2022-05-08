#!/bin/bash

cd "/home/ermesa/Programming Projects/python/cronpip"
source ./bin/activate
echo "#######################" >> snapintime.log
echo "Starting snapshots" >> snapintime.log
python -m snapintime.create_local_snapshots >> snapintime.log
echo "######################" >> snapintime.log
