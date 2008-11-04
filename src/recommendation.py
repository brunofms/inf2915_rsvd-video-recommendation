#!/usr/bin/python

# Gustavo Soares Souza
# Recommendation script based on a midiaId
# Usage: cat videoplayer_AAAAMMDDHH.log | python userMapper.py | python recommendation.py

from collections import defaultdict 
import sys
from math import sqrt

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



# Returns a distance-based similarity score for person1 and person2
def sim_distance(prefs,person1,person2):
	print 'sim_distance called'
	# Get the list of shared_items
	si={}
	for item in prefs[person1]:
		if item in prefs[person2]:
			si[item]=1
	
	# if they have no ratings in common, return 0
	if len(si)==0: return 0
	
	# Add up the squares of all the differences
	sum_of_squares=sum([pow(prefs[person1][item]-prefs[person2][item],2)
						for item in prefs[person1] if item in prefs[person2]])

	return 1/(1+sum_of_squares)

# Returns the best matches for person from the prefs dictionary.
# Number of results and similarity function are optional params.
def topMatches(prefs,person,n=5,similarity=sim_distance):
	print 'topMatcher called'
	scores=[(similarity(prefs,person,other),other)
			for other in prefs if other!=person]

	# Sort the list so the highest scores appear at the top
	scores.sort( )
	scores.reverse( )
	
	return scores[0:n]
	

#testing recommendation
print topMatches(viewers, '7cb0cfbc378bf961605afa2cc940b33b', 10)
