Snap-in-Time
============

![Lint and PyTest](https://github.com/djotaku/Snap-in-Time/workflows/Lint,PyTest,%20MyPy,%20and%20Coverage/badge.svg) [![Documentation Status](https://readthedocs.org/projects/snap-in-time/badge/?version=latest)](https://snap-in-time.readthedocs.io/en/latest/?badge=latest)

script for btrfs backups to create hourly snapshots, remote backups, and cull the snapshots.

See the examples directory for some examples of scripts that could be used to run this program. Ideally, you'd be
running it hourly since snapshots don't take up a lot of space unless you have a large file that's constantly changing (like a large database).

Documentation: https://snap-in-time.readthedocs.io/en/latest/
