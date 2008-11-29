#!/usr/bin/python

# Bruno de F. Melo e Souza
# Usage: cat ../data/treino/ratings/dataset_treino.txt | python userRatingsReducer.py
 
from operator import itemgetter
import sys
 
# maps users to their counts
video2count = {}
rated2count = {}
 
# input comes from STDIN:
# user								midia_id	rating
# fffd233f278af93444e99117cfcbeb3c	898847		5
for line in sys.stdin:
	try:
		# parse the input we got from userMapper.py
		user, midia_id, rating = line.split('\t')

		# remove leading and trailing whitespace
		user = user.strip()
		midia_id = midia_id.strip()
		rating = rating.strip()

		video2count[midia_id] = video2count.get(midia_id, 0) + 1

	except Exception, why:
        # count was not a number, so silently
        # ignore/discard this line
		#print 'Passing...', why
		pass

for video, rated in video2count.items():
	try:
		rated2count[rated] = rated2count.get(rated, 0) + 1
	except ValueError:
		# ignore/discard this line
		pass
 
# write the results to STDOUT (standard output)
for rated, count in rated2count.items():
    print '%s\t%s'% (rated, count)
