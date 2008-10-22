#!/usr/bin/env python
 
from operator import itemgetter
import sys
 
# maps users to their counts
user2count = {}
viewed2count = {}
 
# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
 
    # parse the input we got from userMapper.py
    user, midia_id = line.split('\t', 1)
    # convert count (currently a string) to int
    try:
        user2count[user] = user2count.get(user, 0) + 1
    except ValueError:
        # count was not a number, so silently
        # ignore/discard this line
        pass

for user, viewed in user2count.items():
	try:
		viewed2count[viewed] = viewed2count.get(viewed, 0) + 1
	except ValueError:
		# count was not a number, so silently
		# ignore/discard this line
		pass
 
# sort the words lexigraphically;
#
# this step is NOT required, we just do it so that our
# final output will look more like the official Hadoop
# word count examples
#sorted_user2count = sorted(user2count.items(), key=itemgetter(0))
 
# write the results to STDOUT (standard output)
for viewed, count in viewed2count.items():
    print '%s\t%s'% (viewed, count)