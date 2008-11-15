#!/usr/bin/python

# Bruno de F. Melo e Souza
# Gustavo Soares Souza
# Project Parser

import time
from collections import defaultdict
from operator import itemgetter
import sys, fileinput, os

file_userdistribution = "new_user_distribution.xls"
file_videodistribution = "new_video_distribution.xls"

mediaUserDict = defaultdict(dict)
media_matrix = []
user2count = defaultdict(dict)
video2count = defaultdict(dict)
user_index = {}
video_index = {}
count_lines = 0

filename = "../data/dataset.txt"

# Parses de dataset file
def parseDataSet() :
	inicio = time.time()
	print 'parsing dataset %s ...' % filename
	# TODO: read from a lot of log files
	for line in fileinput.input(filename):
		try:

			(user, media) = line.split()
			view_rate = 1

			mediaUserDict[user][media] = view_rate
			user2count[user] = user2count.get(user, 0) + 1
			video2count[media] = (video2count.get(media, 0)) + 1

		except 	Exception, why:
	        # count was not a number, so silently
	        # ignore/discard this line
			#print "Passing...", why
			pass

	elapsed(inicio)
	
# Returns elapsed time acording to the start time
def elapsed(inicio):
	print 'done'
	fim = time.time()
	elapsed = (fim - inicio) / 60
	print 'duracao: %f min' % elapsed
	
##############
## MAIN ######
##############

parseDataSet()


#######################################
# Cria vetores w e q com chute inicial#
#######################################
user_file = open("user_distribution.xls", "w")
video_file = open("video_distribution.xls", "w")
i = 0
j = 0
w = []
q = []
taxa = 0.001
initial_guess = 0.1

print 'criando o vetor w com o chute inicial'
inicio = time.time()

for user_item in user2count.keys():
	linha = '%s\t%s\n' % (user_item, user2count[user_item])
	user_file.write(linha)
	w.append(initial_guess)
	
elapsed(inicio)

print 'criando o vetor q com o chute inicial'
inicio = time.time()

for video_item in video2count.keys():
	linha = '%s\t%s\n' % (video_item, video2count[video_item])
	video_file.write(linha)
	q.append(initial_guess)
	
elapsed(inicio)

user_file.close();
video_file.close();

########################################
# Popula a matriz ######################
########################################
inicio = time.time()
print 'criando a matriz esparsa...'
for users in mediaUserDict.keys():
        dict_aux = mediaUserDict[users]
        lista = []
        for midias_key in dict_aux.keys():
                lista.append(dict_aux[midias_key])
        media_matrix.append(lista)

elapsed(inicio)

##################################
print '\n'
print 'Total de usuarios: %s' % len(w)
print 'Total de videos: %s' % len(q)
