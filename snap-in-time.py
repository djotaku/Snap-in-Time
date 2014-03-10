__author__ = "Eric Mesa"
__version__ = "v0.2"
__license__ = "GNU GPL v3.0"
__copyright__ = "(c) 2014 Eric Mesa"
__email__ = "ericsbinaryworld at gmail dot com"

import sys, time,subprocess,glob

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
    print "*********************************"
    print "Hey, I'm in snapshot!!"
    print "btrfs snapshot will go in: %s" % snapshotfolder
    print "*********************************\n"
  else:
    command = "sudo btrfs sub snapshot -r /home %s" % snapshotfolder
    subprocess.call(command, shell=True) #don't need sudo if run as root
    
  
def Copysnapshot(debugging):
  """Copy the latest snapshot to the backup folder."""
  if(debugging):
    print "*********************************"
    print "Hey, I'm copying the snapshot!"
    print "*********************************\n"

def getdate():
  """Generates the values for the date variables"""
  Year = time.strftime("%Y")
  Month = time.strftime("%m")
  Day = time.strftime("%d")
  Hour = time.strftime("%H")
  Minute = time.strftime("%M")
  return (Year,Month,Day,Hour,Minute)

def createpriordays(today):
  """Create numbers for searching for day"""
  days = []
  for n in range(1,int(today)-1):
    print n
    days.append(n)
  return days

def dailycleanup(debugging,folder,year,month,day):
  """Keep 2 days worth of backups. After that, only keep 4 backups per day - ideally split by six hours.
  Here's where things get tough. This is super easy to do if the computer's on 24 hours a day. But what if it's sporadically turned off?
  Then how do we determine which ones to get rid of?"""
  deletionfoldersPhase1 = []
  deletionfolders0000to0559 = []
  deletionfolders0600to1159 = []
  deletionfolders1200to1759 = []
  deletionfolders1800to2359 = []
  if(debugging):
    print "*********************************"
    print "Hey, I'm in dailycleanup!!"
    print "folder: %s" % folder
    print "year: %s" % year
    print "month: %s" % month
    print "day: %s" % day
    days = createpriordays(day)
    print "Days: %s" % days
    for n in range(0,len(days)):
      deletionfoldersPhase1.append(glob.glob("test-folder-deletion/%s-%s-%02d*" % (year,month,days[n])))
    deletionfoldersPhase1 = filter(None,deletionfoldersPhase1) #gets rid of empty elements. Usually will only happen if computer isn't on at least once per day
    print "deletionfoldersPhase1: %s" % deletionfoldersPhase1
    for n in range(0,len(deletionfoldersPhase1)):
      for i in range(0,len(deletionfoldersPhase1[n])):
	if len(deletionfoldersPhase1[n]) == 1:
	  print "too small"
	else:
	  print "folder is: %s" % deletionfoldersPhase1[n][i]
	  entiretime = deletionfoldersPhase1[n][i][-4:]
	  print "entire time is %s" % entiretime
	  print "hour tens place is: %s" % entiretime[0]
	  print "hour is: %s" % entiretime[1]
	  print "whole hour is: %s" % entiretime[0:2]
	  if int(deletionfoldersPhase1[n][i][-4]) == 0 and (0 <= int(deletionfoldersPhase1[n][i][-3]) < 6):
	    deletionfolders0000to0559.append(deletionfoldersPhase1[n][i])
	  elif int(deletionfoldersPhase1[n][i][-4]) == 0 and (6 <= int(deletionfoldersPhase1[n][i][-3]) < 10):
	    deletionfolders0600to1159.append(deletionfoldersPhase1[n][i])
	  elif int(deletionfoldersPhase1[n][i][-4]) == 1 and (0 <= int(deletionfoldersPhase1[n][i][-3]) < 2):
	    deletionfolders0600to1159.append(deletionfoldersPhase1[n][i])
	  elif int(deletionfoldersPhase1[n][i][-4]) == 1 and (2 <= int(deletionfoldersPhase1[n][i][-3]) < 8):
	    deletionfolders1200to1759.append(deletionfoldersPhase1[n][i])
	  elif int(deletionfoldersPhase1[n][i][-4]) == 1 and (8 <= int(deletionfoldersPhase1[n][i][-3]) < 10):
	    deletionfolders1800to2359.append(deletionfoldersPhase1[n][i])
	  elif int(deletionfoldersPhase1[n][i][-4]) == 2 and (0 <= int(deletionfoldersPhase1[n][i][-3]) < 4):
	    deletionfolders1800to2359.append(deletionfoldersPhase1[n][i])
    print "deletionfolders0000to0559: %s" % deletionfolders0000to0559
    print "deletionfolders0600to1159: %s" % deletionfolders0600to1159
    print "deletionfolders1200to1759: %s" % deletionfolders1200to1759
    print "deletionfolders1800to2359: %s" % deletionfolders1800to2359
    print "*********************************\n"
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
  print "localfolder: %s" % localfolder
  print "\n"
snapshot(debugit,localfolder)
Copysnapshot(debugit)
dailycleanup(debugit,localfolderbase,Year,Month,Day)