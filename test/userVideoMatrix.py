#!/usr/bin/python

# Bruno de F. Melo e Souza
# Implement a dictionary of viewers and their ratings for a set of videos
# Usage: cat videoplayer_AAAAMMDDHH.log | python userMapper.py | python userVideoMatrix.py

from collections import defaultdict 
import sys
 
# maps users to their counts
#viewers = {}
viewers = defaultdict(dict)
 
# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
	line = line.strip()

	# parse the input we got from userMapper.py
	user, midia_id = line.split('\t', 1)

	try:
		# TODO: gosto como uma fracao do percentual baixado
		# video : gosto
		viewers[user][midia_id] = 1

	except ValueError:
        # count was not a number, so silently
        # ignore/discard this line
		pass

# write the results to STDOUT (standard output)
for user in viewers.keys():
	print user
	for midia_id in viewers[user].keys():
		print '\t%s\t%s'% (midia_id, viewers[user][midia_id])