#!/bin/bash

cd "/home/ermesa/Programming Projects/python/cronpip"
source ./bin/activate
echo "#######################" >> snapintime.log
echo "Starting remote backups" >> snapintime.log
python -m snapintime.remote_backup >> snapintime.log
echo "######################" >> snapintime_remote.log
