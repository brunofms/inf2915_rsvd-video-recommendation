#!/usr/bin/python

# Gustavo Soares Souza
# Recommendation script based on a midiaId
# Usage: cat videoplayer_AAAAMMDDHH.log | python userMapper.py | python recommendation.py

from collections import defaultdict 
import sys
from datetime import *
from math import sqrt

# maps users to their counts
#viewers = {}
viewers = defaultdict(dict)

print ' constructing viewers table' 
# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
	line = line.strip()

	# parse the input we got from userMapper.py
	user, midia_id = line.split('\t', 1)
	try:
		# TODO: gosto como uma fracao do percentual baixado
		viewers[user.strip()][midia_id] = 1

	except ValueError:
        # count was not a number, so silently
        # ignore/discard this line
		pass
print ' done'

# Returns a distance-based similarity score for person1 and person2
def sim_distance(prefs,person1,person2):
	#print 'sim_distance called'
	# Get the list of shared_items
	#print 'comparing %s (%s) with %s (%s)' % (person1, prefs[person1.strip()], person2, prefs[person2])
	si={}
	for item in prefs[person1]:
		if item in prefs[person2]:
			si[item]=1
	
	# if they have nothing in common, return 0
	if len(si)==0: 
		#print 'nothing in common'
		return 0
	
	# Add up the squares of all the differences
	sum_of_squares=sum([pow(prefs[person1][item]-prefs[person2][item],2)
						for item in prefs[person1] if item in prefs[person2]])
	distance = 1/(1+sum_of_squares)
	#if distance < 1 and distance > 0: 
		#print distance
	return distance

# Returns the best matches for person from the prefs dictionary.
# Number of results and similarity function are optional params.
def topMatches(prefs,user,n=5,similarity=sim_distance):
	print 'topMatcher called'
	scores=[(similarity(prefs,user,other),other)
			for other in prefs.keys() if other!=user]

	# Sort the list so the highest scores appear at the top
	scores.sort()
	scores.reverse()
	print 'done'
	return scores[0:n]

#invert the dictionary passed as argument
def invertDict(viewers):
	result={}
	for user in viewers:
		for midia_id in viewers[user]:
			result.setdefault(midia_id,{})
	
			# Flip item and person
			result[midia_id][user]=viewers[user][midia_id]
	
	return result
		
#testing recommendation
print 'user_based:'
print topMatches(viewers, '7cb0cfbc378bf961605afa2cc940b33b', 10)
print '*' * 100
#print 'item_based:'
#item_based = invertDict(viewers)
#print topMatches(viewers, '894047', 10)
