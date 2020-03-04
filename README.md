Snap-in-Time
============

script for btrfs backups to create hourly snapshots & backups and cull the snapshots & backups.

The script should be added to root's cron job (or the user, but to really work correctly should have the sudoers file edited to let this script run without a password) running hourly.
(use "which python" on the commandline to make sure it'll run without changing the first line)

# Overhaul - starting 20200303

God, what a mess I made back in 2014. Holy moly, look at that mess: https://github.com/djotaku/Snap-in-Time/tree/b7f1af14aca489a87d9263bdeeeab4d69cdab584 . Lines 51-150 are recreating something that I anticipate will be a cakewalk using built-in modules. Ugh! Anyway, the overhaul branch will be me starting mostly from scratch and doing this correctly, using Pythonic principles and, generally, not sucking like what I wrote 6 years ago.

# Origins of my culling algorithm

I'm basing it on a conversation I had in the btrfs mailing list. Here's how the guy who inspired me, Duncan, explained it to me:

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
