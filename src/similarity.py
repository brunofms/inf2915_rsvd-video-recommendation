#!/usr/bin/python

# Bruno de F. Melo e Souza
# Gustavo Soares Souza
# Project Library

from math import sqrt
from numpy.linalg import *
from numpy import *
from operator import itemgetter

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
	
# Invert the dictionary passed as argument
def invertDict(mediaUserDict):
	result={}
	for user in mediaUserDict:
		for midia_id in mediaUserDict[user]:
			result.setdefault(midia_id,{})

			# Flip item and person
			result[midia_id][user]=mediaUserDict[user][midia_id]

	return result

# Return a multidimensional array from a dictionary passed as argument
def getArrayFromDict(dict):
        matriz = []
        for users in critics.keys():
                dict_aux = critics[users]
                lista = []
                for midias_key in dict_aux.keys():
                        lista.append(dict_aux[midias_key])
                matriz.append(lista)
        return matriz

#############
## SVD ######
#############

# TODO: Refactory: spatial reduction funtions to a separate file reduction.py

# Returns svd components such as a = u*sigma*qT
def svd_components(a):
	u,sigma,q = svd(a, full_matrices = 1, compute_uv = 1)
	#sigma = diag(sigma)
	q = transpose(q)
	return (u, sigma, q)

# Returns reduced components u and q passed as argument to a 2D space and also
# the inverted matrix of the eigenvalue	
def svd_reduce(u, sigma, q):
	#first and second column from u 
	u2 = u[:,:2]
	
	#first and second column from q
	q2 = q[:,:2]

	#first two eigenvalue
	eigenvalues = diag(sigma[0:2])
	
	return (u2, q2, inv(eigenvalues))

# Reduces an array of data passed as argument to a 2D space
# Example:
# Consider the data_array to be [5 5 0 0 0 5], then the dataembed
# returned would be something like [[-0.37752201 -0.08020351]], depending
# of the values of u2 and eigenvalues_inversed passed as argument. 
def data_2D(data_array, u2, eigenvalues_inversed):
	dataembed = mat(data_array) * mat(u2) * mat(eigenvalues_inversed)
	return dataembed

# Returns a dict with the cossine similarity
def sim_cos(q2, dataembed):
	#number of lines in q
	lines_q = size(q2,0)
	
	user_sim= {}
	count = 1
	for row in xrange(lines_q):
		x = q2[row,:]
		x_t = transpose(x)
		dataembed_t = transpose(dataembed)
		dot_product = dot(mat(x_t),mat(dataembed_t))
		numerator = norm(dot_product)
		denominator = norm(x) * norm(dataembed)
		cossine = numerator / denominator
		user_sim[count] = cossine
		count = count + 1
	
	return sorted(user_sim.items(), key=itemgetter(1), reverse=True)

# Build the complete dataset of similar items
# Off-line processing
def calculateSimilarItems(mediaUserDict, n=10):
	# Create a dictionary of items showing which other items they
	# are most similar to.
	result={}

	# Preference matrix already item centric!

	c=0
	for item in mediaUserDict.keys():
		# Status updates for large datasets
		c+=1
		if c%100==0: print "%d / %d" % (c, len(mediaUserDict))

		# Find the most similar items to this one
		scores=similarity.topMatches(mediaUserDict, item, n, similarity.sim_distance)

		result[item]=scores

	return result
