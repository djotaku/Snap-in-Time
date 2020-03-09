======
Usage
======

Grab config.json from the Github repo (https://github.com/djotaku/Snap-in-Time), edit it, and place it in $HOME/.config/snapintime (or /root/.config/snapintime/ if you're going to run as root)

Creating Local Snapshots
^^^^^^^^^^^^^^^^^^^^^^^^

If running from a git clone:

.. code-block:: Bash
   
   pip -r requirements.txt 
   cd snapintime
   python create_local_snapshots.py

If running from PyPi, run: python -m snapintime.create_local_snapshots


If you want to run it from cron in a virtual environment, you can adapt the following shell script to your situation:

.. code-block:: Bash

    #!/bin/bash
    cd "/home/ermesa/Programming Projects/python/cronpip"
    source ./bin/activate
    python -m snapintime.create_local_snapshots 
    
Make it executable and have cron run that script as often as you like.


Backing Up to Remote Location
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This code makes the assumption that you have setup ssh keys to allow you to ssh to the remote machine without inputting a password. It is recommended to run the remote backup code BEFORE the culling code to increase the chances that the last snapshot on the remote system is still on the local system. (This will minimize the amounnt of data that has to be transferred to the remote system.

.. code-block:: Bash
   
   pip -r requirements.txt 
   cd snapintime
   python remote_backup.py

If running from PyPi, run: python -m snapintime.remote_backup

Culling Local Snapshots
^^^^^^^^^^^^^^^^^^^^^^^

The culling follows the following specification:

- Three days ago: Leave at most 4 snapshots behind - closest snapshots to 0000, 0600, 1200, and 1800. (implemented)
- Seven days ago: Leave at most 1 snapshot behind - the last one that day. In a perfect situation, it would be the one taken at 1800.
- After a quarter (defined as 13 weeks) - Leave at most 1 snapshot per week.
- After a year (52 weeks) - Leave at most 1 snapshot per quarter

I recommend running culling submodule AFTER remote backup (if you're doing the remote backups). This is to prevent the removal of the subvol you'd use for the btrfs send/receive. If your computer is constantly on without interruption, it shouldn't be an issue if you're doing your remote backups daily. And why wouldn't you? The smaller the diff betwen the last backup and this one, the less data you have to send over the network. So it's more of a precaution in case you turn it off for a while on vacation or the computer breaks for a while and can't do the backups.

.. code-block:: Bash
   
   pip -r requirements.txt 
   cd snapintime
   python culling.py

If running from PyPi, run: python -m snapintime.culling
