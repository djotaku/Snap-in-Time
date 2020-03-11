Snap-in-Time
============

![Lint,PyTest, MyPy, and Coverage](https://github.com/djotaku/Snap-in-Time/workflows/Lint,PyTest,%20MyPy,%20and%20Coverage/badge.svg) [![codecov](https://codecov.io/gh/djotaku/Snap-in-Time/branch/master/graph/badge.svg)](https://codecov.io/gh/djotaku/Snap-in-Time) [![Documentation Status](https://readthedocs.org/projects/snap-in-time/badge/?version=latest)](https://snap-in-time.readthedocs.io/en/latest/?badge=latest)

script for btrfs backups to create hourly snapshots & backups and cull the snapshots & backups.

The script should be added to root's cron job (or the user, but to really work correctly should have the sudoers file edited to let this script run without a password) running hourly.

Documentation: https://snap-in-time.readthedocs.io/en/latest/

# Overhaul - starting 20200303

God, what a mess I made back in 2014. Holy moly, look at that mess: https://github.com/djotaku/Snap-in-Time/tree/b7f1af14aca489a87d9263bdeeeab4d69cdab584 . Lines 51-150 are recreating something that I anticipate will be a cakewalk using built-in modules. Ugh! Anyway, the overhaul branch will be me starting mostly from scratch and doing this correctly, using Pythonic principles and, generally, not sucking like what I wrote 6 years ago.
