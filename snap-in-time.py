__author__ = "Eric Mesa"
__version__ = "v0.2"
__license__ = "GNU GPL v3.0"
__copyright__ = "(c) 2014 Eric Mesa"
__email__ = "ericsbinaryworld at gmail dot com"

import sys,time,subprocess,glob,os

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
	  if (0 <= int(entiretime[0:2]) < 6):
	    deletionfolders0000to0559.append(deletionfoldersPhase1[n][i])
	  elif (6 <= int(entiretime[0:2]) < 12):
	    deletionfolders0600to1159.append(deletionfoldersPhase1[n][i])
	  elif (12 <= int(entiretime[0:2]) < 18):
	    deletionfolders1200to1759.append(deletionfoldersPhase1[n][i])
	  elif (18 <= int(entiretime[0:2]) < 24):
	    deletionfolders1800to2359.append(deletionfoldersPhase1[n][i])
    print "deletionfolders0000to0559: %s" % deletionfolders0000to0559
    print "deletionfolders0600to1159: %s" % deletionfolders0600to1159
    print "deletionfolders1200to1759: %s" % deletionfolders1200to1759
    print "deletionfolders1800to2359: %s" % deletionfolders1800to2359
    tokeep = "0000"
    for n in range(0,len(deletionfolders0000to0559)):
      if int(deletionfolders0000to0559[n][-3]) > int(tokeep[-3]) :
	tokeep = deletionfolders0000to0559[n]
    print "deletionfolders0000to0559 before filter: %s" % deletionfolders0000to0559
    print "to keep is: %s" % tokeep
    deletionfolders0000to0559 = [v for v in deletionfolders0000to0559 if v not in tokeep]
    print "deletionfolders0000to0559 after filter: %s" % deletionfolders0000to0559
    
    tokeep = "0000"
    for n in range(0,len(deletionfolders0600to1159)):
      if int(deletionfolders0600to1159[n][-4:]) > int(tokeep[-4:]) :
	tokeep = deletionfolders0600to1159[n]
    print "deletionfolders0600to1159 before filter: %s" % deletionfolders0600to1159
    print "to keep is: %s" % tokeep
    deletionfolders0600to1159 = [v for v in deletionfolders0600to1159 if v not in tokeep]
    print "deletionfolders0600to1159 after filter: %s" % deletionfolders0600to1159
    
    tokeep = "0000"
    for n in range(0,len(deletionfolders1200to1759)):
      if int(deletionfolders1200to1759[n][-4:]) > int(tokeep[-4:]) :
	tokeep = deletionfolders1200to1759[n]
    print "deletionfolders1200to1759 before filter: %s" % deletionfolders1200to1759
    print "to keep is: %s" % tokeep
    deletionfolders1200to1759 = [v for v in deletionfolders1200to1759 if v not in tokeep]
    print "deletionfolders1200to1759 after filter: %s" % deletionfolders1200to1759
    
    tokeep = "0000"
    for n in range(0,len(deletionfolders1800to2359)):
      if int(deletionfolders1800to2359[n][-4:]) > int(tokeep[-4:]) :
	tokeep = deletionfolders1800to2359[n]
    print "deletionfolders1800to2359 before filter: %s" % deletionfolders1800to2359
    print "to keep is: %s" % tokeep
    deletionfolders1800to2359 = [v for v in deletionfolders1800to2359 if v not in tokeep]
    print "deletionfolders1800to2359 after filter: %s" % deletionfolders1800to2359
    
    #time to remove the folders
    for n in deletionfolders0000to0559:
      command = "rmdir $HOME/bin/python/Snap-in-Time/Snap-in-Time/%s" % n
      print command
      #subprocess.call(command,shell=True)
      curr_env = os.environ.copy()
      #print curr_env
      subprocess.Popen(command,env=curr_env,shell=True)
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