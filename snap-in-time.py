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
  """Keep 2 days worth of backups. After that, only keep 4 backups per day - ideally separated by six hours.
  Currently will not properly handle things when it's the 1st or 2nd of the month."""
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
    print "For debug we want the folder to be a bit different"
    folder = "test-folder-deletion"
    print "New folder: %s" % folder
    for n in range(0,len(days)):
      deletionfoldersPhase1.append(glob.glob("%s/%s-%s-%02d*" % (folder,year,month,days[n])))
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
    print "deletionfolders0000to0559 before filter: %s\n" % deletionfolders0000to0559
    print "to keep is: %s\n" % tokeep
    deletionfolders0000to0559 = [v for v in deletionfolders0000to0559 if v not in tokeep]
    print "deletionfolders0000to0559 after filter: %s\n" % deletionfolders0000to0559
    
    tokeep = "0000"
    for n in range(0,len(deletionfolders0600to1159)):
      if int(deletionfolders0600to1159[n][-4:]) > int(tokeep[-4:]) :
	tokeep = deletionfolders0600to1159[n]
    print "deletionfolders0600to1159 before filter: %s\n" % deletionfolders0600to1159
    print "to keep is: %s\n" % tokeep
    deletionfolders0600to1159 = [v for v in deletionfolders0600to1159 if v not in tokeep]
    print "deletionfolders0600to1159 after filter: %s\n" % deletionfolders0600to1159
    
    tokeep = "0000"
    for n in range(0,len(deletionfolders1200to1759)):
      if int(deletionfolders1200to1759[n][-4:]) > int(tokeep[-4:]) :
	tokeep = deletionfolders1200to1759[n]
    print "deletionfolders1200to1759 before filter: %s\n" % deletionfolders1200to1759
    print "to keep is: %s\n" % tokeep
    deletionfolders1200to1759 = [v for v in deletionfolders1200to1759 if v not in tokeep]
    print "deletionfolders1200to1759 after filter: %s\n" % deletionfolders1200to1759
    
    tokeep = "0000"
    for n in range(0,len(deletionfolders1800to2359)):
      if int(deletionfolders1800to2359[n][-4:]) > int(tokeep[-4:]) :
	tokeep = deletionfolders1800to2359[n]
    print "deletionfolders1800to2359 before filter: %s\n" % deletionfolders1800to2359
    print "to keep is: %s\n" % tokeep
    deletionfolders1800to2359 = [v for v in deletionfolders1800to2359 if v not in tokeep]
    print "deletionfolders1800to2359 after filter: %s\n" % deletionfolders1800to2359
    
    #time to remove the folders
    for n in deletionfolders0000to0559:
      command = "rmdir $HOME/bin/python/Snap-in-Time/Snap-in-Time/%s" % n
      print command
      #subprocess.call(command,shell=True)
      curr_env = os.environ.copy()
      #print curr_env
      subprocess.Popen(command,env=curr_env,shell=True)
    
    for n in deletionfolders0600to1159:
      command = "rmdir $HOME/bin/python/Snap-in-Time/Snap-in-Time/%s" % n
      print command
      #subprocess.call(command,shell=True)
      curr_env = os.environ.copy()
      #print curr_env
      subprocess.Popen(command,env=curr_env,shell=True)
 
    for n in deletionfolders1200to1759:
      command = "rmdir $HOME/bin/python/Snap-in-Time/Snap-in-Time/%s" % n
      print command
      #subprocess.call(command,shell=True)
      curr_env = os.environ.copy()
      #print curr_env
      subprocess.Popen(command,env=curr_env,shell=True)
     
    for n in deletionfolders1800to2359:
      command = "rmdir $HOME/bin/python/Snap-in-Time/Snap-in-Time/%s" % n
      print command
      #subprocess.call(command,shell=True)
      curr_env = os.environ.copy()
      #print curr_env
      subprocess.Popen(command,env=curr_env,shell=True)     
    print "*********************************\n"
  else:
    days = createpriordays(day)
    for n in range(0,len(days)):
      deletionfoldersPhase1.append(glob.glob("%s/%s-%s-%02d*" % (folder,year,month,days[n])))
    deletionfoldersPhase1 = filter(None,deletionfoldersPhase1) #gets rid of empty elements. Usually will only happen if computer isn't on at least once per day
    for n in range(0,len(deletionfoldersPhase1)):
      for i in range(0,len(deletionfoldersPhase1[n])):
	if len(deletionfoldersPhase1[n]) == 1:
	  print "too small"
	else:
	  entiretime = deletionfoldersPhase1[n][i][-4:]
	  if (0 <= int(entiretime[0:2]) < 6):
	    deletionfolders0000to0559.append(deletionfoldersPhase1[n][i])
	  elif (6 <= int(entiretime[0:2]) < 12):
	    deletionfolders0600to1159.append(deletionfoldersPhase1[n][i])
	  elif (12 <= int(entiretime[0:2]) < 18):
	    deletionfolders1200to1759.append(deletionfoldersPhase1[n][i])
	  elif (18 <= int(entiretime[0:2]) < 24):
	    deletionfolders1800to2359.append(deletionfoldersPhase1[n][i])
    tokeep = "0000"
    for n in range(0,len(deletionfolders0000to0559)):
      if int(deletionfolders0000to0559[n][-3]) > int(tokeep[-3]) :
	tokeep = deletionfolders0000to0559[n]
    deletionfolders0000to0559 = [v for v in deletionfolders0000to0559 if v not in tokeep]
    
    tokeep = "0000"
    for n in range(0,len(deletionfolders0600to1159)):
      if int(deletionfolders0600to1159[n][-4:]) > int(tokeep[-4:]) :
	tokeep = deletionfolders0600to1159[n]
    deletionfolders0600to1159 = [v for v in deletionfolders0600to1159 if v not in tokeep]
    
    tokeep = "0000"
    for n in range(0,len(deletionfolders1200to1759)):
      if int(deletionfolders1200to1759[n][-4:]) > int(tokeep[-4:]) :
	tokeep = deletionfolders1200to1759[n]
    deletionfolders1200to1759 = [v for v in deletionfolders1200to1759 if v not in tokeep]
    
    tokeep = "0000"
    for n in range(0,len(deletionfolders1800to2359)):
      if int(deletionfolders1800to2359[n][-4:]) > int(tokeep[-4:]) :
	tokeep = deletionfolders1800to2359[n]
    deletionfolders1800to2359 = [v for v in deletionfolders1800to2359 if v not in tokeep]
    
    #time to remove the folders - needs to be fixed before used in production
    for n in deletionfolders0000to0559:
      command = "sudo btrfs subvolume delete %s" % n
      print command
      subprocess.call(command,shell=True)
    
    for n in deletionfolders0600to1159:
      command = "sudo btrfs subvolume delete %s" % n
      print command
      subprocess.call(command,shell=True)

 
    for n in deletionfolders1200to1759:
      command = "sudo btrfs subvolume delete %s" % n
      print command
      subprocess.call(command,shell=True)

     
    for n in deletionfolders1800to2359:
      command = "sudo btrfs subvolume delete %s" % n
      print command
      subprocess.call(command,shell=True)

def createpriordaysforweekly(thismonth,today):
  """Create numbers for searching for day"""
  days = []
  days2 = [[],[]]
  months = []
  for n in range(1,int(today)-6):
    print n
    days.append(n)
  if(len(days)<7): #also need to modify days to match up with months
    if int(thismonth) == 1:
      months = ["12","1"]
      for n in range(0,7-len(days)):
	days2[0].append(31-n)
      days2[1]=list(days)
    else:
      months = [str(int(thismonth)-1),thismonth]
      for n in range(0,7-len(days)):
	if months[0] == "2":
	  days2[0].append(28-n)
	elif months[0] == "1" or "3" or "5" or "7" or "8" or "10" or "12":
	  days2[0].append(31-n)
	elif months[0] == "4" or "6" or "9" or "11":
	  days2[0].append(30-n)
      days2[1]=list(days)
  else:
    months = [thismonth]
    days2 = list(days)
  return (months,days2)

def weeklycleanup(debugging,folder,year,month,day):
  """Leave One week of backups with the previous frequency: 4 backups per day.
  For weeks prior to this one, eliminite 3/4 of those, leaving one per day."""
  deletionfoldersPhase1 = []
  
  if(debugging):
    print "*********************************"
    print "Hey, I'm in weeklycleanup!!"
    print "folder: %s" % folder
    print "year: %s" % year
    print "month: %s" % month
    print "day: %s" % day
    print "*********************************\n"
    (months,days) = createpriordaysforweekly(month,day)
    print "Days: %s" % days
    print "len(days[0]): %s" % len(days[0])
    print "len(days[1]): %s" % len(days[1])
    print "Months: %s" % months
    print "For debug we want the folder to be a bit different"
    folder = "test-folder-deletion"
    print "New folder: %s" % folder
  else:
    print "something soon"
  if len(months) == 1:
    for n in range(0,len(days)):
	deletionfoldersPhase1.append(glob.glob("%s/%s-%s-%02d*" % (folder,year,months,days[n])))
	deletionfoldersPhase1 = filter(None,deletionfoldersPhase1) #gets rid of empty elements. Usually will only happen if computer isn't on at least once per day
	print "deletionfoldersPhase1: %s" % deletionfoldersPhase1
  elif len(months) == 2:
    for n in range(0,len(days[0])):
	deletionfoldersPhase1.append(glob.glob("%s/%s-%02d-%02d*" % (folder,year,int(months[0]),days[0][n])))
    deletionfoldersPhase1 = filter(None,deletionfoldersPhase1) #gets rid of empty elements. Usually will only happen if computer isn't on at least once per day
    print "deletionfoldersPhase1: %s\n" % deletionfoldersPhase1
    for n in range(0,len(days[1])):
	deletionfoldersPhase1.append(glob.glob("%s/%s-%02d-%02d*" % (folder,year,int(months[1]),days[1][n])))
    deletionfoldersPhase1 = filter(None,deletionfoldersPhase1) #gets rid of empty elements. Usually will only happen if computer isn't on at least once per day
    print "deletionfoldersPhase1: %s" % deletionfoldersPhase1

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
#weeklycleanup(debugit,localfolderbase,Year,Month,Day)