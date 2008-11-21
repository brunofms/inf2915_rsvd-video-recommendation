#!/usr/local/bin/python

# Bruno de F. Melo e Souza
# Gustavo Soares Souza
# Project Parser

import time
from collections import defaultdict
from operator import itemgetter
import sys, fileinput, os
from copy import copy
import pdb
from math import *
#pdb.set_trace()

mediaUserDict = defaultdict(dict)
user2count = defaultdict(dict)
video2count = defaultdict(dict)
user_index = {}
video_index = {}
######################
# Parametros do svd ##
######################
#TEST_DATASET_FILE = '../data/teste/views/dataset_1.txt'
TEST_DATASET_FILE = '../data/teste/ratings/dataset_teste.txt'
#TEST_DATASET_FILE = '../data/dataset_treino_netflix.txt'
#TRAIN_DATASET_FILE = '../data/treino/views/dataset_0.txt'
TRAIN_DATASET_FILE = '../data/treino/ratings/dataset_treino.txt'
#TRAIN_DATASET_FILE = '../data/dataset_treino_netflix.txt'
lrate = 0.001
INITIAL_GUESS = 0.1
NUM_VARIAVEL_LATENTE = 10
NUM_PASSOS = 10
MIN_IMPROVEMENT = 0.0001
w = {}
q = {}
lista_variaveis_latente_w = []
lista_variaveis_latente_q = []
count_lines = 0

# Parses de dataset file
def parseDataSet():
	inicio = time.time()
	print 'parsing dataset %s ...' % TRAIN_DATASET_FILE
	# TODO: read from a lot of log files
	for line in fileinput.input(TRAIN_DATASET_FILE):
		try:
			#pdb.set_trace()
			(user, media, rating) = line.split()
			user = user.strip()
			media = media.strip()
			rating = rating.strip()
			
			rating = int(rating)
			mediaUserDict[user][media] = rating
			user2count[user] = user2count.get(user, 0) + 1
			video2count[media] = (video2count.get(media, 0)) + 1

		except 	Exception, why:
	        # count was not a number, so silently
	        # ignore/discard this line
			#print "Passing...", why
			pass

	elapsed(inicio)


def trainData():
	#######################################
	# Cria vetores w e q com chute inicial#
	#######################################
	#Arquivos para gerarem graficos no excel com a distribuicao dos dados
	user_file_distribution = open("user_distribution.xls", "w")
	video_file_distribution = open("video_distribution.xls", "w")
	i = 0
	j = 0

	print 'criando o vetor w com o chute inicial'
	inicio = time.time()

	for user_item in user2count.keys():
		linha = '%s\t%s\n' % (user_item, user2count[user_item])
		user_index[user_item] = i
		user_file_distribution.write(linha)
		w[user_item] = INITIAL_GUESS
		i = i + 1
	
	elapsed(inicio)

	print 'criando o vetor q com o chute inicial'
	inicio = time.time()

	for video_item in video2count.keys():
		linha = '%s\t%s\n' % (video_item, video2count[video_item])
		video_index[video_item] = j
		video_file_distribution.write(linha)
		q[video_item] = INITIAL_GUESS
		j = j + 1
	
	elapsed(inicio)

	user_file_distribution.close()
	video_file_distribution.close()

	print '*' * 60
	print 'Total de usuarios: %s' % len(w)
	print 'Total de videos: %s' % len(q)
	print '*' * 60
	
	print 'comecando o treino...'
	print 'lrate: %f' % lrate
	print 'chute inicial: %f' % INITIAL_GUESS
	print 'variaveis latente: %d' % NUM_VARIAVEL_LATENTE
	print 'passos: %d' % NUM_PASSOS
	inicio = time.time()

	q_log = open("vetor_q.log", "w")
	w_log = open("vetor_w.log", "w")
	rmse_last=1000000
	for k in range(NUM_VARIAVEL_LATENTE):
		print 'obtendo a variavel latente =>>>> %d' % k
		rmse_last=1000
		for i_passos in range(NUM_PASSOS):
			aux = 0
			sq = 0
			for user_item in w.keys():
				for video_item in mediaUserDict[user_item].keys():
					#print '%s -> %s' % (user_item, video_item)
					rating = mediaUserDict[user_item][video_item]
					aux = aux + 1
					if i_passos > 0:
						#err = lrate * (rating - predictRating(user_item,video_item))
						err = rating - predictRating(user_item,video_item)
					else:
						#err = lrate * (rating -  (w[user_item]*q[video_item]))
						err = rating - (w[user_item] * q[video_item])
					#w[user_item] = w[user_item] + (err * q[video_item])
					#q[video_item] = q[video_item] + (err * w[user_item])
					sq = sq + (err**2)
					lerr = lrate * err
					tmp = lerr * w[user_item]
					w[user_item] = w[user_item] + (lerr * q[video_item])
					q[video_item] = q[video_item] + tmp
			rmse = sqrt(sq/aux)
			print 'passo %d - RMSE: %f = sqrt(%f/%d)' % (i_passos+1, rmse, sq, aux)
			if rmse > rmse_last - MIN_IMPROVEMENT:
				break
			else:
				rmse_last = rmse
			
		lista_variaveis_latente_w.append(copy(w))
		lista_variaveis_latente_q.append(copy(q))
		
	#fim do calculo da variavel latente	
	#w_log.write(str(lista_variaveis_latente_w)+'\n')
	#q_log.write(str(lista_variaveis_latente_q)+'\n')
	q_log.close()
	w_log.close()
	elapsed(inicio)

def predictRating(user, midia):
	#print 'predicting rating...'
	#inicio = time.time()
	_rating = 1.0
	#print '%d variaveis latentes' % len(lista_variaveis_latente_w)
	for z in xrange(len(lista_variaveis_latente_w)):
		_w = lista_variaveis_latente_w[z]
		_q = lista_variaveis_latente_q[z]
		_rating = _rating + (_w[user] * _q[midia])
		# http://www.timelydevelopment.com/demos/NetflixPrize.aspx
		if _rating > 5:
			_rating = 5
		elif _rating < 1:
			_rating = 1
	#elapsed(inicio)
	#print '*' * 60
	return _rating

def testData(_w,_q):
	inicio = time.time()
	print 'iniciando o teste...'
	i=0
	err = 0.0
    # le o dataset de testes
	for line in fileinput.input(TEST_DATASET_FILE):
		try:
			line.strip()
			user,media,rating = line.split()
			user = user.strip()
			media = media.strip()
			rating = rating.strip()
			rating = int(rating)
			
			if _w.has_key(user) and _q.has_key(media):
				predicted = float(_w[user] * _q[media])
				#print 'rating: %f, predicted: %f' % (rating, predicted)
				err = err + (rating - predicted)**2
				if (i%300) == 0:
					print 'err: %f - rating: %f, predicted: %f = %f * %f' % (err, rating, predicted, _w[user], _q[media])
				i = i + 1

		except Exception, why:
			pass

	mse = err / i
	rmse = sqrt(mse)
	elapsed(inicio)

	print '************************************************************'	
	print 'MSE: %f' % mse
	print 'Total de usuarios com rating estimado: %d' % i

	return rmse
	
# Returns elapsed time acording to the start time
def elapsed(inicio):
	print 'done'
	fim = time.time()
	elapsed = (fim - inicio) / 60
	print 'duracao: %f min' % elapsed

def main():
	parseDataSet()
	trainData()
	_rmse = testData(w,q)
	print 'lrate: %f' % lrate
	print 'chute inicial: %f' % INITIAL_GUESS
	print 'variaveis latente: %d' % NUM_VARIAVEL_LATENTE
	print 'passos: %d' % NUM_PASSOS
	print '>>>>> RMSE: %f' % _rmse
	
##############
## MAIN ######
##############

main()
