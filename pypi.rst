

.. image:: https://codecov.io/gh/djotaku/Snap-in-Time/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/djotaku/Snap-in-Time

.. image:: https://readthedocs.org/projects/snap-in-time/badge/?version=latest
    :target: https://snap-in-time.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

snapintime is meant to manage the creation, culling, and send to a remote location of btrfs snapshots.

As of version 0.11.0, it creates snapshots, culls local snapshots three days old, a week old, and for the previous quarter.
It can also btrfs send/receive to a remote btrfs subvol.

Culling:

- Three days ago: Leave at most 4 snapshots behind - closest snapshots to 0000, 0600, 1200, and 1800. (implemented)
- Seven days ago: Leave at most 1 snapshot behind - the last one that day. In a perfect situation, it would be the one taken at 1800. (implemented)
- After a quarter (defined as 13 weeks) - Leave at most 1 snapshot per week. (implemented)
- After a year (52 weeks) - Leave at most 1 snapshot per quarter (implemented)

Documentation can be found at: https://snap-in-time.readthedocs.io/en/latest/
