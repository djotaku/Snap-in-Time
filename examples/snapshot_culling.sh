#!/bin/bash

cd "/home/ermesa/Programming Projects/python/cronpip"
source ./bin/activate
echo "#######################" >> snapintime_culling.log
echo "Starting culling" >> snapintime_culling.log
python -m snapintime.culling >> snapintime_culling.log
echo "######################" >> snapintime_culling.log
