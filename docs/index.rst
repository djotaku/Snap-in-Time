.. snapintime documentation master file, created by
   sphinx-quickstart on Tue Mar  3 19:43:16 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to snapintime's documentation!
======================================

snapintime is meant to manage the creation, culling, and send to a remote location of btrfs snapshots.

At this point in time it just creates snapshots.

Grab config.json from the Github repo (https://github.com/djotaku/Snap-in-Time), edit it, and place it in $HOME/.config/snapintime

Then run python -m snapintime.create_local_snapshots

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   
   modules/create_local_snapshots



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
