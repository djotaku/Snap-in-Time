#!/bin/bash

cd "/home/ermesa/Programming Projects/python/cronpip"
source ./bin/activate
echo "#######################" >> snapintime_remote.log
echo "Starting remote backups" >> snapintime_remote.log
python -m snapintime.remote_backup >> snapintime_remote.log
echo "######################" >> snapintime_remote.log
