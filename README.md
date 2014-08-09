Snap-in-Time
============

script for btrfs backups to create hourly snapshots & backups and cull the snapshots & backups.

The script should be added to root's cron job (or the user, but to really work correctly should have the sudoers file edited to let this script run without a password) running hourly.
(use "which python" on the commandline to make sure it'll run without changing the first line)

For right now here's what the script does:
-create snapshots as often as it's run. Intended to run hourly, but you could do it with whatever frequency you want: minutes, hours, days, etc
-Every third day it removes all but at most 4 snapshots for the day three days ago. It does its best to make sure these are as close to 6 hours apart as possible.

Here're my snapshots after a few days:
# btrfs sub list /home
ID 275 gen 8892 top level 5 path home
ID 1021 gen 8847 top level 275 path .snapshots
ID 1025 gen 1775 top level 275 path .snapshots/2014-03-13-2300
ID 1032 gen 2284 top level 275 path .snapshots/2014-03-14-0500
ID 1037 gen 2587 top level 275 path .snapshots/2014-03-14-0900
ID 1038 gen 2667 top level 275 path .snapshots/2014-03-14-1700
ID 1044 gen 3305 top level 275 path .snapshots/2014-03-14-2300
ID 1050 gen 3986 top level 275 path .snapshots/2014-03-15-0500
ID 1057 gen 4674 top level 275 path .snapshots/2014-03-15-1100
ID 1064 gen 5301 top level 275 path .snapshots/2014-03-15-1700
ID 1071 gen 5909 top level 275 path .snapshots/2014-03-15-2300
ID 1072 gen 5993 top level 275 path .snapshots/2014-03-16-0000
ID 1073 gen 6082 top level 275 path .snapshots/2014-03-16-0100
ID 1074 gen 6164 top level 275 path .snapshots/2014-03-16-0200
ID 1075 gen 6251 top level 275 path .snapshots/2014-03-16-0300
ID 1076 gen 6333 top level 275 path .snapshots/2014-03-16-0400
ID 1077 gen 6419 top level 275 path .snapshots/2014-03-16-0500
ID 1078 gen 6502 top level 275 path .snapshots/2014-03-16-0600
ID 1079 gen 6590 top level 275 path .snapshots/2014-03-16-0700
ID 1080 gen 6676 top level 275 path .snapshots/2014-03-16-0800
ID 1081 gen 6770 top level 275 path .snapshots/2014-03-16-0900
ID 1083 gen 6877 top level 275 path .snapshots/2014-03-16-1000
ID 1084 gen 6982 top level 275 path .snapshots/2014-03-16-1100
ID 1085 gen 7087 top level 275 path .snapshots/2014-03-16-1200
ID 1086 gen 7194 top level 275 path .snapshots/2014-03-16-1300
ID 1087 gen 7300 top level 275 path .snapshots/2014-03-16-1400
ID 1089 gen 7403 top level 275 path .snapshots/2014-03-16-1500
ID 1090 gen 7507 top level 275 path .snapshots/2014-03-16-1600
ID 1091 gen 7610 top level 275 path .snapshots/2014-03-16-1700
ID 1092 gen 7710 top level 275 path .snapshots/2014-03-16-1800
ID 1094 gen 7812 top level 275 path .snapshots/2014-03-16-1900
ID 1095 gen 7914 top level 275 path .snapshots/2014-03-16-2000
ID 1096 gen 8013 top level 275 path .snapshots/2014-03-16-2100
ID 1097 gen 8090 top level 275 path .snapshots/2014-03-16-2200
ID 1098 gen 8137 top level 275 path .snapshots/2014-03-16-2300
ID 1099 gen 8187 top level 275 path .snapshots/2014-03-17-0000
ID 1100 gen 8251 top level 275 path .snapshots/2014-03-17-0100
ID 1101 gen 8302 top level 275 path .snapshots/2014-03-17-0200
ID 1102 gen 8356 top level 275 path .snapshots/2014-03-17-0300
ID 1103 gen 8459 top level 275 path .snapshots/2014-03-17-0400
ID 1104 gen 8524 top level 275 path .snapshots/2014-03-17-0500
ID 1105 gen 8576 top level 275 path .snapshots/2014-03-17-0600
ID 1106 gen 8628 top level 275 path .snapshots/2014-03-17-0700
ID 1107 gen 8685 top level 275 path .snapshots/2014-03-17-0800
ID 1108 gen 8738 top level 275 path .snapshots/2014-03-17-0900
ID 1109 gen 8793 top level 275 path .snapshots/2014-03-17-1000
ID 1110 gen 8847 top level 275 path .snapshots/2014-03-17-1100

You can see that it is working correctly on the daily level.


Future things it will do:
-Send them to a backup drive so they will actually protect against hardware failure
-Similar culling on the weekly, quarterly, and yearly scale. I'm basing it on a conversation I had in the btrfs mailing list. Here's how the guy who inspired me, Duncan, explained it to me:

"However, best snapshot management practice does progressive snapshot 
thinning, so you never have more than a few hundred snapshots to manage 
at once.  Think of it this way.  If you realize you deleted something you 
needed yesterday, you might well remember about when you deleted it and 
can thus pick the correct snapshot to mount and copy it back from.  But 
if you don't realize you need it until a year later, say when you're 
doing your taxes, how likely are you to remember the specific hour, or 
even the specific day, you deleted it?  A year later, getting a copy from 
the correct week, or perhaps the correct month, will probably suffice, 
and even if you DID still have every single hour's snapshots a year 
later, how would you ever know which one to pick?  So while a day out, 
hourly snapshots are nice, a year out, they're just noise.

As a result, a typical automated snapshot thinning script, working with 
snapshots each hour to begin with, might look like this:

Keep two days of hourly snapshots: 48 hourly snapshots

After two days, delete five of six snapshots, leaving a snapshot every 6 
hours, four snapshots a day, for another 5 days: 4*5=20 6-hourly, 20
+48=68 total.

After a week, delete three of the four 6-hour snapshots, leaving daily 
snapshots, for 12 weeks (plus the week of more frequent snapshots above, 
13 weeks total): 7*12=84 daily snaps, 68+84=152 total.

After a quarter (13 weeks), delete six of seven daily snapshots, leaving 
weekly snapshots, for 3 more quarters plus the one above of more frequent 
snapshots, totaling a year: 3*13=39 weekly snaps, 152+39=191 total.

After a year, delete 12 of the 13 weekly snapshots, leaving one a 
quarter.  At 191 for the latest year plus one a quarter you can have 
several years worth of snapshots (well beyond the normal life of the 
storage media) and still be in the low 200s snapshots total, while 
keeping them reasonably easy to manage. =:^)"

Commit dedicated to my toddler daughter who is recovering from surgery yesterday