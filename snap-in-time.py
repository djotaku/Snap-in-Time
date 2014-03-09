__author__ = "Eric Mesa"
__version__ = "v0.1"
__license__ = "GNU GPL v3.0"
__copyright__ = "(c) 2014 Eric Mesa"
__email__ = "ericsbinaryworld at gmail dot com"

import sys

def getargs():
  """Grab the commandline arguments and put them into a list.  Also give help if no arguments provided"""
  try:
        args = sys.argv[1:]
        if args[0]== "debug":
	  debug = True
  except:
	debug = False
  return debug

def snapshot(debugging):
  """"This runs every time the script is run (meant to be hourly). It will create a snapshot in the correct folder. 
  It will not move the snapshots to the backup drive. That will be another function."""
  if(debugging):
    print "Hey, I'm in snapshot!!"
  
def Copysnapshot(debugging):
  """Copy the latest snapshot to the backup folder."""
  if(debugging):
    print "Hey, I'm copying the snapshot!"
  
debugit = getargs()
if(debugit):
  print "Debugging!"
snapshot(debugit)
Copysnapshot(debugit)