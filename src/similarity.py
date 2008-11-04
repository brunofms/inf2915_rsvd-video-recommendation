#!/usr/bin/python

# Bruno de F. Melo e Souza
# Project Library

from math import sqrt

# Returns the Pearson correlation coefficient for media_1 and media_2
def sim_pearson(mediaUserDict, media_1, media_2):
	# Get the list of mutually rated items
	si={}
	for item in mediaUserDict[media_1]:
		if item in mediaUserDict[media_2]:
			si[item]=1

	#Find the number of elements
	n=len(si)
	
	# if they are no ratings in common, return 0
	if n==0:
		return 0

	# Add up all the preferences
	sum1=sum([mediaUserDict[media_1][item] for item in si])
	sum2=sum([mediaUserDict[media_2][item] for item in si])
	
	# Sum up the squares
	sum1Sq=sum([pow(mediaUserDict[media_1][item],2) for item in si])
	sum2Sq=sum([pow(mediaUserDict[media_2][item],2) for item in si])
	
	# Sum up the products
	pSum=sum([mediaUserDict[media_1][item]*mediaUserDict[media_2][item] for item in si])
	
	# Calculate Pearson score
	num=pSum-(sum1*sum2/n)
	den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
	if den==0:
		return 0
	
	r=num/den
	
	return r

# Returns a distance-based similarity score for media_1 and media_2
def sim_distance(mediaUserDict, media_1, media_2):
	# Get the list of shared items
	si={}
	for item in mediaUserDict[media_1]:
		if item in mediaUserDict[media_2]:
			si[item]=1

	# if they have no ratings in common, return 0
	if len(si)==0:
		return 0

	# Add up the squares of all the differences
	sum_of_squares=sum([pow(mediaUserDict[media_1][item]-mediaUserDict[media_2][item],2)
		for item in mediaUserDict[media_1] if item in mediaUserDict[media_2]])

	return 1/(1+sum_of_squares)

# Returns the best matches for a given media from the mediaUserDict dictionary.
# Number of results and similarity function are optional params.
def topMatches(mediaUserDict, media, n=10, similarity=sim_pearson):
	scores=[(similarity(mediaUserDict,media,other),other)
	for other in mediaUserDict.keys() if other!=media]

	# Sort the list so the highest scores appear at the top
	scores.sort()
	scores.reverse()

	return scores[0:n]