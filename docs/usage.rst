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

The culling follows this progressive retention policy. Days are calendar days,
weeks are ISO weeks, and quarters are calendar quarters:

- Keep all hourly snapshots for the most recent two days.
- For the next five days, keep up to four snapshots per calendar day, closest to 0000, 0600, 1200, and 1800.
- For the next twelve weeks, keep one snapshot per calendar day, closest to 1800.
- For the next three quarters, keep one snapshot per ISO week, closest to Sunday at 1800.
- After one year, keep one snapshot per calendar quarter, closest to the end of the quarter at 1800.

The ideal history contains 191 snapshots through the first year, plus one
snapshot per quarter for older history.

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
