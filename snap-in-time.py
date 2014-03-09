__author__ = "Eric Mesa"
__version__ = "v0.1"
__license__ = "GNU GPL v3.0"
__copyright__ = "(c) 2014 Eric Mesa"
__email__ = "ericsbinaryworld at gmail dot com"

import sys

def snapshot():
  """"This runs every time the script is run (meant to be hourly). It will create a snapshot in the correct folder. 
  It will not move the snapshots to the backup drive. That will be another function."""
  print "Hey, I'm in snapshot!!"
  
def Copysnapshot():
  """Copy the latest snapshot to the backup folder."""
  print "Hey, I'm copying the snapshot!"
  
snapshot()
Copysnapshot()