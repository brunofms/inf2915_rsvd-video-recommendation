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
userRatingDict = defaultdict(dict)
video2count = defaultdict(dict)
user2count = defaultdict(dict)

######################
# Parametros do svd ##
######################
TEST_DATASET_FILE = '../data/netflix/dataset_treino.txt'
#TEST_DATASET_FILE = '../data/netflix/dataset.txt'
TRAIN_DATASET_FILE = '../data/netflix/probe_parsed.txt'

MIN_IMPROVEMENT = 0.0001

#populate matrix
def addMatrix(user, media, rating):
	mediaUserDict[user][media] = rating

#gets ratings from matrix
def getRating(user, media):
	rating = mediaUserDict[user].get(media, 0)
	return rating

# Parses de dataset file
def parseDataSet():
	inicio = time.time()
	print 'parsing dataset %s ...' % TEST_DATASET_FILE
	fileIN = open(TEST_DATASET_FILE, "r")
	line = fileIN.readline()
	while line:
		line = line.strip()
		try:
			#pdb.set_trace()
			(user, media, rating) = line.split()
			user = user.strip()
			media = media.strip()
			rating = rating.strip()
			
			rating = int(rating)
			addMatrix(user, media, rating)
			video2count[media] = 1
			user2count[user] = 1

		except 	Exception, why:
	        # count was not a number, so silently
	        # ignore/discard this line
			print "Passing...", why
			pass
		line = fileIN.readline()
	fileIN.close()
	elapsed(inicio)


def trainData(w, q, lrate, INITIAL_GUESS, NUM_VARIAVEL_LATENTE, NUM_PASSOS, lista_variaveis_latente_q, lista_variaveis_latente_w):
	#######################################
	# Cria vetores w e q com chute inicial#
	#######################################
	#Arquivos para gerarem graficos no excel com a distribuicao dos dados
	i = 0
	j = 0

	print 'criando o vetor w com o chute inicial'

	for user_item in user2count.keys():
		w[user_item] = INITIAL_GUESS
		i = i + 1

	print 'criando o vetor q com o chute inicial'
	inicio = time.time()

	for video_item in video2count.keys():
		q[video_item] = INITIAL_GUESS
		j = j + 1
	
	elapsed(inicio)

	print '*' * 60
	print 'Total de usuarios: %s' % len(w)
	print 'Total de videos: %s' % len(q)
	rse_max = 5.0 * 5.0 * len(q)
	print 'RSEMAX: %f' % rse_max
	print '*' * 60
	
	print 'comecando o treino...'
	inicio = time.time()

	rmse_last=1000000
	
	for k in range(NUM_VARIAVEL_LATENTE):
		print 'obtendo a variavel latente =>>>> %d' % k
		for i_passos in range(NUM_PASSOS):
			#aux = 0
			sq = 0
			for user_item in w.keys():
				aux = 0
				for video_item in q.keys():
				#for video_item in mediaUserDict[user_item].keys():
					aux = aux + 1
					#print 'processando video - %d' % aux
					rating = getRating(user_item, video_item)
					if rating == 0:
						continue
					aux = aux + 1
					predicted = 0.0
					if i_passos > 0:
						predicted = predictRating(user_item, video_item, lista_variaveis_latente_w, lista_variaveis_latente_q)
						err = rating - predicted
					else:
						predicted = w[user_item] * q[video_item]
						err = rating - predicted
					sq = sq + (err * err)
					#######
					#REVER#
					#######
					if err > 5.0:
						print 'rating: %f >>> predicted: %f >>> erro: %f' % (rating, predicted, err)
					lerr = lrate * err
					tmp = lerr * w[user_item]
					w[user_item] = w[user_item] + (lerr * q[video_item])
					q[video_item] = q[video_item] + tmp
			if sq > rse_max:
				print 'RSE: %f' % sq
				break
			#rmse = sqrt(sq/aux)
			#print 'passo %d - RMSE: %f = sqrt(%f/%d)' % (i_passos+1, rmse, sq, aux)
			#if rmse > rmse_last - MIN_IMPROVEMENT:
			#	break
			#else:
			#	rmse_last = rmse
			
		lista_variaveis_latente_w.append(copy(w))
		lista_variaveis_latente_q.append(copy(q))
		
	#fim do calculo da variavel latente	
	elapsed(inicio)

def predictRating(user, midia, lista_variaveis_latente_w, lista_variaveis_latente_q):
	#print 'predicting rating...'
	#inicio = time.time()
	_rating = 1.0
	for z in xrange(len(lista_variaveis_latente_w)):
		_w = lista_variaveis_latente_w[z]
		_q = lista_variaveis_latente_q[z]
		_rating = _rating + (_w[user] * _q[midia])
		# http://www.timelydevelopment.com/demos/NetflixPrize.aspx
		if _rating > 5:
			_rating = 5
			break
		elif _rating < 1:
			_rating = 1
			break
	#elapsed(inicio)
	#print '*' * 60
	return _rating

def testData(_w,_q):
	inicio = time.time()
	print 'iniciando o teste...'
	i=0
	err = 0.0
    # le o dataset de testes
	for line in fileinput.input(TRAIN_DATASET_FILE):
		try:
			line.strip()
			user,media = line.split('|')
			user = user.strip()
			media = media.strip()
			if _w.has_key(user) and _q.has_key(media):
				predicted = float(_w[user] * _q[media])
				userRatingDict[user][media] = predicted
			else:
				print 'User: %s e Midia: %s nao encontrados na base' % (user, media)
				userRatingDict[user][media] = 2.5

		except Exception, why:
			pass
	elapsed(inicio)
	
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

def main2(chute=0.1, variaveis_latentes=10, passos=20, lrate=0.001):
	inicio = time.time()
	lrate = 0.001
	INITIAL_GUESS = chute
	NUM_VARIAVEL_LATENTE = variaveis_latentes
	NUM_PASSOS = passos
	MIN_IMPROVEMENT = 0.0001
	w = {}
	q = {}
	lista_variaveis_latente_w = []
	lista_variaveis_latente_q = []
	
	#Chama os metodos
	trainData(w, q, lrate, INITIAL_GUESS, NUM_VARIAVEL_LATENTE, NUM_PASSOS, lista_variaveis_latente_q, lista_variaveis_latente_w)
	print 'testing data...'
	testData(w,q)
	print 'done'
	
	prediction_file = open("predicted_glb_ml.txt", "w")
	for user_item in userRatingDict.keys():
		prediction_file.write('%s:\n' % user_item)
		for video_item in userRatingDict[user_item].keys():
			print '%s\t%s\t%1.2f' % (user_item, video_item, userRatingDict[user_item][video_item])
			prediction_file.write('%1.2f\n' % userRatingDict[user_item][video_item])
			prediction_file.flush()
	prediction_file.close()
	fim = time.time()
	elapsed = (fim - inicio) / 60
	
	return (lrate, INITIAL_GUESS, NUM_VARIAVEL_LATENTE, NUM_PASSOS, elapsed)

##############
## MAIN ######
##############

#main()
inicio = time.time()
parseDataSet()
RESULT_FILE = "result.xls"
result_log = open(RESULT_FILE, "w")
result_log.write('LRATE\tCHUTE\tVARIAVEIS_LATENTES\tPASSOS\tRMSE\tELAPSED\n')
result_log.flush()

MAXIMO_LATENTES = 10
PASSOS_AUX = 1
CHUTE_AUX = 0.1
STEP = 0
print 'Maximo de variaveis latentes: %d' % MAXIMO_LATENTES

(lrate, INITIAL_GUESS, NUM_VARIAVEL_LATENTE, NUM_PASSOS, tempo_decorrido) = main2(CHUTE_AUX, MAXIMO_LATENTES, PASSOS_AUX, 0.001)

print 'lrate: %f' % lrate
print 'chute inicial: %f' % INITIAL_GUESS
print 'variaveis latente: %d' % NUM_VARIAVEL_LATENTE
print 'passos: %d' % NUM_PASSOS
print 'tempo de execucao: %f min' % tempo_decorrido
print '*' * 60


result_log.close()
elapsed(inicio)
print '%s escrito' % RESULT_FILE