.. snapintime documentation master file, created by
   sphinx-quickstart on Tue Mar  3 19:43:16 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to snapintime's documentation!
======================================

snapintime is meant to manage the creation, culling, and send to a remote location of btrfs snapshots.

At this point in time it creates snapshots and can btrfs send/receive to a remote btrfs subvol.


.. toctree::
   :maxdepth: 2
   :caption: Contents:
   
   usage
   config
   modules/create_local_snapshots
   modules/culling
   modules/remote_backup
   modules/utils/config
   modules/utils/date



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
