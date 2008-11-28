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
user2count = defaultdict(dict)
video2count = defaultdict(dict)
user_index = {}
video_index = {}
######################
# Parametros do svd ##
######################
TEST_DATASET_FILE = '../data/netflix/dataset_treino.txt'
#TEST_DATASET_FILE = '../data/netflix/dataset.txt'
TRAIN_DATASET_FILE = '../data/netflix/probe_parsed.txt'

MIN_IMPROVEMENT = 0.0001

# Parses de dataset file
def parseDataSet():
	inicio = time.time()
	print 'parsing dataset %s ...' % TEST_DATASET_FILE
	fileIN = open(sys.argv[1], "r")
	line = fileIN.readline()
	while line:
		print line
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
			print "Passing...", why
			pass
		line = fileIN.readline()

	elapsed(inicio)


def trainData(w, q, lrate, INITIAL_GUESS, NUM_VARIAVEL_LATENTE, NUM_PASSOS, lista_variaveis_latente_q, lista_variaveis_latente_w):
	#######################################
	# Cria vetores w e q com chute inicial#
	#######################################
	#Arquivos para gerarem graficos no excel com a distribuicao dos dados
	user_file_distribution = open("user_distribution.xls", "w")
	video_file_distribution = open("video_distribution.xls", "w")
	i = 0
	j = 0

	print 'criando o vetor w com o chute inicial'

	for user_item in user2count.keys():
		linha = '%s\t%s\n' % (user_item, user2count[user_item])
		user_index[user_item] = i
		user_file_distribution.write(linha)
		w[user_item] = INITIAL_GUESS
		i = i + 1

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
	inicio = time.time()

	rmse_last=1000000
	for k in range(NUM_VARIAVEL_LATENTE):
		print 'obtendo a variavel latente =>>>> %d' % k
		rmse_last=1000
		for i_passos in range(NUM_PASSOS):
			aux = 0
			sq = 0
			for user_item in w.keys():
				for video_item in mediaUserDict[user_item].keys():
					rating = mediaUserDict[user_item][video_item]
					aux = aux + 1
					if i_passos > 0:
						err = rating - predictRating(user_item,video_item, lista_variaveis_latente_w, lista_variaveis_latente_q)
					else:
						err = rating - (w[user_item] * q[video_item])
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
	elapsed(inicio)

def predictRating(user, midia, lista_variaveis_latente_w, lista_variaveis_latente_q):
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
	for line in fileinput.input(TRAIN_DATASET_FILE):
		try:
			line.strip()
			user,media = line.split('|')
			user = user.strip()
			media = media.strip()
			if _w.has_key(user) and _q.has_key(media):
				predicted = float(_w[user] * _q[media])
				userRatingDict[user][media] = predicted

		except Exception, why:
			pass

	
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

MAXIMO_LATENTES = 5
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
