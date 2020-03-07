======
Usage
======

Grab config.json from the Github repo (https://github.com/djotaku/Snap-in-Time), edit it, and place it in $HOME/.config/snapintime (or /root/.config/snapintime/ if you're going to run as root)

Creating Local Snapshots
^^^^^^^^^^^^^^^^^^^^^^^^

If running from a git clone:

.. code::Bash
   
   pip -r requirements.txt 
   cd snapintime
   python create_local_snapshots.py

If running from PyPi, run: python -m snapintime.create_local_snapshots


If you want to run it from cron in a virtual environment, you can adapt the following shell script to your situation:

.. code::Bash

    #!/bin/bash
    cd "/home/ermesa/Programming Projects/python/cronpip"
    source ./bin/activate
    python -m snapintime.create_local_snapshots 
    
Make it executable and have cron run that script as often as you like.


Backing Up to Remote Location
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This code makes the assumption that you have setup ssh keys to allow you to ssh to the remote machine without inputting a password. It is recommended to run the remote backup code BEFORE the culling code to increase the chances that the last snapshot on the remote system is still on the local system. (This will minimize the amounnt of data that has to be transferred to the remote system.

.. code::Bash
   
   pip -r requirements.txt 
   cd snapintime
   python remote_backup.py

If running from PyPi, run: python -m snapintime.remote_backup
