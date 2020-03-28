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

For a more involved script, useful for logging, see `Putting it All Together`_.

Backing Up to Remote Location
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This code makes the assumption that you have setup ssh keys to allow you to ssh to the remote machine without inputting a password. It is recommended to run the remote backup code BEFORE the culling code to increase the chances that the last snapshot on the remote system is still on the local system. (This will minimize the amount of data that has to be transferred to the remote system.

.. code-block:: Bash
   
   pip -r requirements.txt 
   cd snapintime
   python remote_backup.py

If running from PyPi, run: python -m snapintime.remote_backup

Culling Local Snapshots
^^^^^^^^^^^^^^^^^^^^^^^

The culling follows the following specification:

- Three days ago: Leave at most 4 snapshots behind - closest snapshots to 0000, 0600, 1200, and 1800. (implemented)
- Seven days ago: Leave at most 1 snapshot behind - the last one that day. In a perfect situation, it would be the one taken at 1800. (implemented)
- 90 days ago: Go from that date up another 90 days and leave at most 1 snapshot per week. (implemented)
- 365 days ago: Go form that date up another 365 days and leave at most 1 snapshot per quarter (implemented)

(Not going to care about leap years, eventually it'll fix itself if this is run regularly)

I recommend running culling submodule AFTER remote backup (if you're doing the remote backups). This is to prevent the removal of the subvol you'd use for the btrfs send/receive. If your computer is constantly on without interruption, it shouldn't be an issue if you're doing your remote backups daily. And why wouldn't you? The smaller the diff betwen the last backup and this one, the less data you have to send over the network. So it's more of a precaution in case you turn it off for a while on vacation or the computer breaks for a while and can't do the backups.

.. code-block:: Bash
   
   pip -r requirements.txt 
   cd snapintime
   python culling.py

If running from PyPi, run: python -m snapintime.culling

Putting it All Together
^^^^^^^^^^^^^^^^^^^^^^^

Here is my crontab output:

.. code-block:: Bash

    0 * * * * /root/bin/snapshots.sh
    @daily /root/bin/remote_snapshots.sh
    0 4 * * * /root/bin/snapshot_culling.sh

remote_snapshots.sh:

.. code-block:: Bash

    #!/bin/bash

    cd "/home/ermesa/Programming Projects/python/cronpip"
    source ./bin/activate
    echo "#######################" >> snapintime_remote.log
    echo "Starting remote backups" >> snapintime_remote.log
    python -m snapintime.remote_backup >> snapintime_remote.log
    echo "######################" >> snapintime_remote.log
    #!/bin/bash

snapshot_culling.sh:

.. code-block:: Bash

    #!/bin/bash

    cd "/home/ermesa/Programming Projects/python/cronpip"
    source ./bin/activate
    echo "#######################" >> snapintime_culling.log
    echo "Starting culling" >> snapintime_culling.log
    python -m snapintime.culling >> snapintime_culling.log
    echo "######################" >> snapintime_culling.log

snapshots.sh:

.. code-block:: Bash

    #!/bin/bash

    cd "/home/ermesa/Programming Projects/python/cronpip"
    source ./bin/activate
    echo "#######################" >> snapintime.log
    echo "Starting snapshots" >> snapintime.log
    python -m snapintime.create_local_snapshots >> snapintime.log
    echo "######################" >> snapintime.log
