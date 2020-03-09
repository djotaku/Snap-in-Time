snapintime is meant to manage the creation, culling, and send to a remote location of btrfs snapshots.

As of version 0.8.0, it creates snapshots, culls local snapshots three days old, and can btrfs send/receive to a remote btrfs subvol.

Culling:

- Three days ago: Leave at most 4 snapshots behind - closest snapshots to 0000, 0600, 1200, and 1800. (implemented)
- Seven days ago: Leave at most 1 snapshot behind - the last one that day. In a perfect situation, it would be the one taken at 1800.
- After a quarter (defined as 13 weeks) - Leave at most 1 snapshot per week.
- After a year (52 weeks) - Leave at most 1 snapshot per quarter

Documentation can be found at: https://snap-in-time.readthedocs.io/en/latest/