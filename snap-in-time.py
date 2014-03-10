__author__ = "Eric Mesa"
__version__ = "v0.1"
__license__ = "GNU GPL v3.0"
__copyright__ = "(c) 2014 Eric Mesa"
__email__ = "ericsbinaryworld at gmail dot com"

import sys, time

def getargs():
  """Grab the commandline arguments and put them into a list.  Also give help if no arguments provided"""
  try:
        args = sys.argv[1:]
        if args[0]== "debug":
	  debug = True
  except:
	debug = False
  return debug

def snapshot(debugging,snapshotfolder):
  """"This runs every time the script is run (meant to be hourly). It will create a snapshot in the correct folder. 
  It will not move the snapshots to the backup drive. That will be another function."""
  if(debugging):
    print "Hey, I'm in snapshot!!"
    print "btrfs snapshot will go in: %s" % snapshotfolder
  else:
    print "nothing now"
    
  
def Copysnapshot(debugging):
  """Copy the latest snapshot to the backup folder."""
  if(debugging):
    print "Hey, I'm copying the snapshot!"

def getdate():
  """Generates the values for the date variables"""
  Year = time.strftime("%Y")
  Month = time.strftime("%m")
  Day = time.strftime("%d")
  Hour = time.strftime("%H")
  Minute = time.strftime("%M")
  return (Year,Month,Day,Hour,Minute)

#Setting up variables
#dates
(Year,Month,Day,Hour,Minute) = getdate()
localfolder = "/home/.snapshots/%s-%s-%s-%s-%s" % (Year, Month, Day, Hour, Minute)
debugit = getargs()
if(debugit):
  print "Debugging!"
  print localfolder
snapshot(debugit,localfolder)
Copysnapshot(debugit)