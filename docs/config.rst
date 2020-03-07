===========
config.json
===========

An example of the config.json file:

.. code::JSON

    {   "0":
    { "subvol": "/home",
    "backuplocation": "/home/.snapshot",
    "remote": "True",
    "remote_location": "user@server",
    "remote_subvol_dir": "/media/backups"
    },
    "1":
    { "subvol": "/media/Photos",
    "backuplocation": "/media/Photos/.Snapshots"
    },
    "2":
    { "subvol": "/media/Archive",
    "backuplocation": "/media/NotHome/Snapshots/Archive"
    }
    }

 - For the 0, 1, 2, 3, etc - there is currently (as of 0.7.0) any inherent meaning to the fact that they are numbers. They just need to be distinct alpha-numberic sequences.
 - subvol: this should be the subvolume you want to create a snapshot of.
 - backuplocation: the subvolume that holds your backup subvolumes.
 - remote: If set to True, an attempt will be made to backup to the remote location. Any other value or lack of this field means it will not try and backup to the remote location.
 - remote_location: The username@theserver where the backup subvolumes will be sent to.
 - remote_subvol_dir: Just like backuplocation, but on the remote machine.
