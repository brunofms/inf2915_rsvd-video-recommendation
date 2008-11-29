#!/usr/bin/python

# Bruno de F. Melo e Souza
# Usage: cat ../data/treino/ratings/dataset_treino.txt | python videoAvgRatingsReducer.py
 
from operator import itemgetter
import sys
 
# maps users to their counts
user2count = {}
sum2count = {}
avg2count = {}
 
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

		# POG
		user2count[user] = user2count.get(user, 0) + 1
		sum2count[user] = sum2count.get(user, 0) + int(rating)

	except Exception, why:
        # count was not a number, so silently
        # ignore/discard this line
		#print 'Passing...', why
		pass

# POG
avgrating = {}
for user, sum in sum2count.items():
	num = float(sum)
	den = float(user2count[user])
	#print '%s\t%s\t%f' % (sum,user2count[user],num/den)
	avgrating[user] = round(num/den,1)

for user, avg in avgrating.items():
	try:
		avg2count[avg] = avg2count.get(avg, 0) + 1
	except ValueError:
		# ignore/discard this line
		pass
 
# write the results to STDOUT (standard output)
for avg, count in avg2count.items():
    print '%.1f\t%s'% (avg, count)
