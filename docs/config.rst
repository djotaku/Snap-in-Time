===========
config.json
===========

An example of the config.json file:

.. code-block:: JSON

    {   "0":
    { "subvol": "/home",
    "backuplocation": "/home/.snapshot",
    "remote": "True",
    "remote_location": "user@server",
    "remote_subvol_dir": "/media/backups",
    "remote_protected":["2022-02-08-0000", "2022-02-15-0000", "2022-04-26-0000", "2021-10-17-0000", "2022-04-16-0000"]
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

- For the 0, 1, 2, 3, etc - there is currently (as of 0.8.1) not any inherent meaning to the fact that they are numbers. They just need to be distinct alpha-numberic sequences.
- subvol: this should be the subvolume you want to create a snapshot of.
- backuplocation: the subvolume that holds your backup subvolumes.
- remote: If set to True, an attempt will be made to backup to the remote location. Any other value or lack of this field means it will not try and backup to the remote location.
- remote_location: The username@theserver where the backup subvolumes will be sent to.
- remote_subvol_dir: Just like backuplocation, but on the remote machine.
- remote_protected: A list of snapshots you don't want to del
