#!/usr/bin/python

# Bruno de F. Melo e Souza
# Usage: cat videoplayer_AAAAMMDDHH.log | python userMapper.py | python videoReducer.py
 
from operator import itemgetter
import sys
 
# maps users to their counts
video2count = {}
viewed2count = {}
 
# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
	line = line.strip()

	# parse the input we got from userMapper.py
	user, midia_id = line.split('\t', 1)

	try:
		video2count[midia_id] = video2count.get(midia_id, 0) + 1
	except ValueError:
        # count was not a number, so silently
        # ignore/discard this line
		pass

#for midia_id, viewed in video2count.items():
#	print '%s\t%s'% (midia_id, viewed)

for midia_id, viewed in video2count.items():
	try:
		viewed2count[viewed] = viewed2count.get(viewed, 0) + 1
	except ValueError:
		# ignore/discard this line
		pass
 
# write the results to STDOUT (standard output)
for viewed, count in viewed2count.items():
    print '%s\t%s'% (viewed, count)