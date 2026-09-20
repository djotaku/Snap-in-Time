Snap-in-Time
============

![Lint and PyTest](https://github.com/djotaku/Snap-in-Time/workflows/Lint,PyTest,%20MyPy,%20and%20Coverage/badge.svg) [![Documentation Status](https://readthedocs.org/projects/snap-in-time/badge/?version=latest)](https://snap-in-time.readthedocs.io/en/latest/?badge=latest)

script for btrfs backups to create hourly snapshots, remote backups, and cull the snapshots.

See the examples directory for some examples of scripts that could be used to run this program. Ideally, you'd be
running it hourly since snapshots don't take up a lot of space unless you have a large file that's constantly changing (like a large database).

Documentation: https://snap-in-time.readthedocs.io/en/latest/

## AI Usage

From the projects creation in 2014 through to 2024 no AI was used in the production of this codebase.

- For [Release v3.0.0](https://github.com/djotaku/Snap-in-Time/releases/tag/v3.0.0) I used AI for the first time in this codebase to fix a long-standing bug in the culling algorithm that was not working correctly. 
