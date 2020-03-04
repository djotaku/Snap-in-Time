#!/usr/bin/python

__author__ = "Eric Mesa"
__version__ = "v0.1"
__license__ = "GNU GPL v3.0"
__copyright__ = "(c) 2018 Eric Mesa"
__email__ = "ericsbinaryworld at gmail dot com"

import sys,time,subprocess,glob,os

def snapshot(snapshotfolder):
  """"This runs every time the script is run (meant to be hourly). It will create a snapshot in the correct folder. 
  It will not move the snapshots to the backup drive. That will be another function."""
  command = "/usr/sbin/btrfs sub snapshot -r /home %s" % snapshotfolder #added full path to btrfs so it would work in cron
  subprocess.call(command, shell=True) #don't need sudo if run as root    

def getdate():
  """Generates the values for the date variables"""
  Year = time.strftime("%Y")
  Month = time.strftime("%m")
  Day = time.strftime("%d")
  Hour = time.strftime("%H")
  Minute = time.strftime("%M")
  return (Year,Month,Day,Hour,Minute)

def createpriordaysmaster(thismonth,today,whichrange):
  """Create numbers for searching for day
  thismonth is the number for the month (ie 1-12)
  today is today's date (the day number (ie 1-31)
  whichrange is used to determine if this is daily, weekly, quarterly, or yearly"""
  days = []
  days2 = [[],[]]
  months = []
  if whichrange == "daily":
    if int(today) > 3:
      for n in range(2,1,-1):
	days.append(int(today)-n)
      months = thismonth
      days2 = list(days)
    else:
      for n in range(2,1,-1):
	if int(today)-n > 0:
	  days.append(int(today)-n)
	  
      if int(thismonth) == 1:
	months = "12" 
	for n in range(2-len(days),1,-1):
	  days.append((31+2)-n)
	days2=list(days)
      else:
	months =str(int(thismonth)-1)
	if months[0] == "2":
	    if today == "2":
	      days = [28]
	    else:
	      days = [27]
	elif months[0] == "1" or months[0] == "3" or months[0] == "5" or months[0] == "7" or months[0] == "8" or months[0] == "10" or months[0] == "12":
	    if today == "2":
	      days = [31]
	    else:
	      days = [30]
	elif months[0] == months[0] == "4" or months[0] == "6" or months[0] == "9" or months[0] == "11":
	    if today == "2":
	      days = [30]
	    else:
	      days = [29]
	days2=list(days)
	  
  elif whichrange == "weekly":
    if int(today) > 13:
      for n in range(13,6,-1):
	days.append(int(today)-n)
      months = [thismonth]
      days2 = list(days)
    elif 6 < int(today) < 14:
      for n in range(13,6,-1):
	if int(today)-n > 0:
	  days.append(int(today)-n)
      
      if int(thismonth) == 1:
	months = ["12","1"]
	for n in range(13-len(days),6,-1):
	  days2[0].append((31+7)-n)
	days2[1]=list(days)
      else:
	months = [str(int(thismonth)-1),thismonth]
	for n in range(13-len(days),6,-1):
	  if months[0] == "2":
	    days2[0].append((28+7)-n)
	  elif months[0] == "1" or months[0] == "3" or months[0] == "5" or months[0] == "7" or months[0] == "8" or months[0] == "10" or months[0] == "12":	    
	    days2[0].append((31+7)-n)
	  elif months[0] == "4" or months[0] == "6" or months[0] == "9" or months[0] == "11":
	    days2[0].append((30+7)-n)
	days2[1]=list(days)
    else:
      for n in range(13,6,-1):
	if int(today)-n > 0:
	  days.append(int(today)-n)
      
      if int(thismonth) == 1:
	months = ["12","1"]
	for n in range(13-len(days),6,-1):
	  days2[0].append((31+7)-n)
	days2[1]=list(days)
      else:
	months = [str(int(thismonth)-1),thismonth]
	for n in range(13-len(days),6,-1):
	  if months[0] == "2":
	    days2[0].append((28+int(today))-n)
	  elif months[0] == "1" or "3" or "5" or "7" or "8" or "10" or "12":	    
	    days2[0].append((31+int(today))-n)
	  elif months[0] == "4" or "6" or "9" or "11":
	    days2[0].append((30+int(today))-n)
  elif whichrange == "quarterly":
    days2 = list(days)
    if thismonth == "1" or thismonth == "2" or thismonth == "3":
      print "Not handling last year yet!"
    elif thismonth == "4" or thismonth == "5" or thismonth == "6":
      months = list(['1','2','3'])
    elif thismonth == "7" or thismonth == "8" or thismonth == "9":
      months = list(['4','5','6'])
    elif thismonth == "10" or thismonth == "11" or thismonth == "12":
      months = list(['7','8','9'])  
  elif whichrange == "yearly":
    print "yearly"
    
  return (months,days2)
    
def btrfsdeletion(folderlist):
  tokeep = "0000"
  for n in range(0,len(folderlist)):
    if (int(folderlist[n][-4])*10 + int(folderlist[n][-3])) > (int(tokeep[-4])*10 + int(tokeep[-3])) :
	tokeep = folderlist[n]
  folderlist = [v for v in folderlist if v not in tokeep]
  
  #time to remove the btrfs
  for n in folderlist:
    #command = "sudo btrfs subvolume delete %s" % n
    command = "/usr/sbin/btrfs subvolume delete %s" % n #added full path so command would work in cron
    print command
    subprocess.call(command,shell=True)
    
def dailycleanup(folder,year,month,day):
  """Keep 2 days worth of backups. After that, only keep 4 backups per day - ideally separated by six hours.
  Currently will not properly handle things when it's the 1st or 2nd of the month."""
  deletionfoldersPhase1 = []
  deletionfolders0000to0559 = []
  deletionfolders0600to1159 = []
  deletionfolders1200to1759 = []
  deletionfolders1800to2359 = []
  #days = createpriordays(day)
  (months,days) = createpriordaysmaster(month,day,"daily") #fix for prior month?
  for n in range(0,len(days)):
      deletionfoldersPhase1.append(glob.glob("%s/%s-%s-%02d*" % (folder,year,months,days[n])))
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
      
      btrfsdeletion(deletionfolders0000to0559)
      btrfsdeletion(deletionfolders0600to1159)
      btrfsdeletion(deletionfolders1200to1759)
      btrfsdeletion(deletionfolders1800to2359)
      
      #start over for next day
      deletionfoldersPhase1 = [] 
      deletionfolders0000to0559 = []
      deletionfolders0600to1159 = []
      deletionfolders1200to1759 = []
      deletionfolders1800to2359 = []

  
if __name__=="__main__":
  #Setting up variables
  #dates
  (Year,Month,Day,Hour,Minute) = getdate()
  localfolderbase = "/home/.snapshots"
  localfolder = "%s/%s-%s-%s-%s%s" % (localfolderbase,Year, Month, Day, Hour, Minute)
  snapshot(localfolder)
  dailycleanup(localfolderbase,Year,Month,Day)
