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
#TRAIN_DATASET_FILE = '../data/netflix/dataset_treino.txt'
TRAIN_DATASET_FILE = '../data/netflix/dataset.txt'
TEST_DATASET_FILE = '../data/netflix/probe_parsed.txt'
NETFLIX_DATASET_DIR='../data/netflix/download/training_set'

MIN_IMPROVEMENT = 0.0001

#populate matrix
def addMatrix(user, media, rating):
	mediaUserDict[media][user] = rating

#gets ratings from matrix
def getRating(user, media):
	rating = mediaUserDict[media].get(user, 0)
	return rating

# Parses de dataset file
def parseDataSet():
	inicio = time.time()
	print 'parsing dataset %s ...' % TRAIN_DATASET_FILE
	fileIN = open(TRAIN_DATASET_FILE, "r")
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
			#addMatrix(user, media, rating)
			video2count[media] = 1
			user2count[user] = 1

		except 	Exception, why:
	        # count was not a number, so silently
	        # ignore/discard this line
			print "Passing... -> %s" % why
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
		q[user_item] = INITIAL_GUESS
		i = i + 1

	print 'criando o vetor q com o chute inicial'
	inicio = time.time()

	for video_item in video2count.keys():
		w[video_item] = INITIAL_GUESS
		j = j + 1
	
	elapsed(inicio)

	print '*' * 60
	print 'Total de usuarios: %s' % len(q)
	print 'Total de videos: %s' % len(w)
	#para limitar o RMSE em 3.0
	soma_rse_max = 3.0 * len(w) * len(q)
	print 'SOMA RSE MAX: %f' % soma_rse_max
	print '*' * 60
	
	print 'comecando o treino...'
	inicio = time.time()

	rmse_last=1000000
	
	for k in range(NUM_VARIAVEL_LATENTE):
		print 'obtendo a variavel latente =>>>> %d' % k
		inicio = time.time()
		for i_passos in range(NUM_PASSOS):
			################################
			# Read dir of movie.txt files ##
			################################
			sq = 0
			for file_item in os.listdir(NETFLIX_DATASET_DIR):
				movie_filename = '%s/%s' % (NETFLIX_DATASET_DIR, file_item)
				#print 'lendo %s' % movie_filename
				i = 0
				for line in fileinput.input(movie_filename):
					i = i + 1
					#try:
					if i == 1:
						end=line.find(':')
						video_item=line[0:end]
					else:
						user_item,rating,date=line.split(',')
						rating = int(rating)
						predicted = 0.0
						if i_passos > 0:
							predicted = predictRating(user_item, video_item, lista_variaveis_latente_w, lista_variaveis_latente_q)
							err = rating - predicted
						else:
							predicted = w[video_item] * q[user_item]
							err = rating - predicted
						sq = sq + (err * err)
						#######
						#REVER#
						#######
						if err > 5.0:
							print 'rating: %f >>> predicted: %f >>> erro: %f' % (rating, predicted, err)
						lerr = lrate * err
						tmp = lerr * w[video_item]
						w[video_item] = w[video_item] + (lerr * q[user_item])
						q[user_item] = q[user_item] + tmp	
					#except Exception, why:
					#	print 'Erro!! -> %s' % why
					#	pass
			########
			if sq > soma_rse_max:
				print 'Soma RSE (%f) passou o limite: %f (breakin)' % (sq, soma_rse_max)
				break
			#rmse = sqrt(sq/aux)
			#print 'passo %d - RMSE: %f = sqrt(%f/%d)' % (i_passos+1, rmse, sq, aux)
			#if rmse > rmse_last - MIN_IMPROVEMENT:
			#	break
			#else:
			#	rmse_last = rmse
			elapsed(inicio)
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
		_rating = _rating + (_w[midia] * _q[user])
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
	for line in fileinput.input(TEST_DATASET_FILE):
		#try:
		line.strip()
		user,media = line.split()
		user = user.strip()
		media = media.strip()
		if _w.has_key(media) and _q.has_key(user):
			predicted = float(_w[media] * _q[user])
			if (predicted > 5.0):
				predicted = 5.0
			elif (predicted < 1.0):
				predicted = 1.0
			userRatingDict[media][user] = predicted
		else:
			print 'User: %s e Midia: %s nao encontrados na base' % (user, media)
			userRatingDict[media][user] = 2.5

		#except Exception, why:
		#	pass
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
	for video_item in sorted(userRatingDict.iterkeys()):
		prediction_file.write('%s:\n' % video_item)
		for user_item in userRatingDict[video_item].keys():
			#print '%d\t%s\t%1.2f' % (video_item, user_item, userRatingDict[video_item][user_item])
			prediction_file.write('%1.2f\n' % userRatingDict[video_item][user_item])
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

MAXIMO_LATENTES = 1
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
