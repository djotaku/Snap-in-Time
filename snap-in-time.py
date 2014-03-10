__author__ = "Eric Mesa"
__version__ = "v0.1"
__license__ = "GNU GPL v3.0"
__copyright__ = "(c) 2014 Eric Mesa"
__email__ = "ericsbinaryworld at gmail dot com"

import sys, time,subprocess

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
    command = "sudo btrfs sub snapshot -r /home %s" % snapshotfolder
    subprocess.call(command, shell=True) #don't need sudo if run as root
    
  
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

def dailycleanup(debugging,folder,month,day):
  """Keep 2 days worth of backups. After that, only keep 4 backups per day - ideally split by six hours.
  Here's where things get tough. This is super easy to do if the computer's on 24 hours a day. But what if it's sporadically turned off?
  Then how do we determine which ones to get rid of?"""
  if(debugging):
    print "Hey, I'm in dailycleanup!!"
    print "folder: %s" % folder
    print "month: %s" % month
    print "day: %s" % day
  else:
    print "will do stuff soon"

#Setting up variables
#dates
(Year,Month,Day,Hour,Minute) = getdate()
localfolderbase = "/home/.snapshots"
localfolder = "%s/%s-%s-%s-%s%s" % (localfolderbase,Year, Month, Day, Hour, Minute)
debugit = getargs()
if(debugit):
  print "Debugging!"
  print localfolder
snapshot(debugit,localfolder)
Copysnapshot(debugit)
dailycleanup(debugit,localfolderbase,Month,Day)