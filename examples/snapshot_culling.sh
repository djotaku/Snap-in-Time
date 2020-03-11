#!/bin/bash

cd "/home/ermesa/Programming Projects/python/cronpip"
source ./bin/activate
echo "#######################" >> snapintime.log
echo "Starting culling" >> snapintime.log
python -m snapintime.culling >> snapintime.log 
echo "######################" >> snapintime_culling.log
