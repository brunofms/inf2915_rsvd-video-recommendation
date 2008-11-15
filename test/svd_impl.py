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

filename = "/Users/gustavosoares/repos/git/video-recommendation/data/dataset.txt"

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
user_file_distribution = open("user_distribution.xls", "w")
video_file_distribution = open("video_distribution.xls", "w")
matrix_xls = open("media_matrix.xls", "w")
i = 0
j = 0
w = []
q = []
lrate = 0.001
initial_guess = 0.1

print 'criando o vetor w com o chute inicial'
inicio = time.time()

for user_item in user2count.keys():
	linha = '%s\t%s\n' % (user_item, user2count[user_item])
	user_index[user_item] = i
	user_file_distribution.write(linha)
	w.append(initial_guess)
	i = i + 1
	
elapsed(inicio)

print 'criando o vetor q com o chute inicial'
inicio = time.time()

for video_item in video2count.keys():
	linha = '%s\t%s\n' % (video_item, video2count[video_item])
	video_index[video_item] = j
	video_file_distribution.write(linha)
	q.append(initial_guess)
	j = j + 1
	
elapsed(inicio)

user_file_distribution.close()
video_file_distribution.close()

########################################
# Popula a matriz ######################
########################################
linha = ''
inicio = time.time()
print 'criando a matriz esparsa...'

for users in mediaUserDict.keys():
        dict_aux = mediaUserDict[users]
        lista = []
        for midias_key in dict_aux.keys():
                linha = linha + '%d\t' % dict_aux[midias_key]
                lista.append(dict_aux[midias_key])
        media_matrix.append(lista)
        matrix_xls.write(linha+'\n')
        linha = ''



elapsed(inicio)
matrix_xls.close()
##################################
print '\n'
print 'Total de usuarios: %s' % len(w)
print 'Total de videos: %s' % len(q)

import pdb
###################
## BEGING SVD #####
###################
inicio = time.time()
print 'SVD running...'
#pdb.set_trace()
err = 0
for i_aux in range(i):
	print 'w[i_aux] antes: %f' % w[i_aux]
	#print 'obtendo o vetor w aproximado para o usuario %d' % i_aux
	for j_aux in range(j):
		'''print 'j_aux: %d' % j_aux
		print 'q[j_aux]: %f' % q[j_aux]
		print 'i_aux: %d' % i_aux
		print 'w[i_aux]: %f' % w[i_aux]'''
		Aij = 0
		try:
			Aij = media_matrix[i_aux][j_aux]
		except Exception:
			pass
		#print 'media_matrix[i_aux][j_aux]: %f' % Aij
		#print 'erro antes: %f' % err
		err = err + (Aij - (q[j_aux] * w[i_aux])) * q[j_aux]
		#print 'erro depois: %f' % err
	w[i_aux] = w[i_aux] + (lrate * err)
	print 'w[i_aux] depois: %f' % w[i_aux]
	err = 0

elapsed(inicio)

print 'w: \n%s' % w
print '*' * 60
print 'q: \n%s' % q