#!/usr/local/bin/python

# Bruno de F. Melo e Souza
# Gustavo Soares Souza
# Project Parser

import time
from collections import defaultdict
from operator import itemgetter
import sys, fileinput, os
import pdb

videos = 0
videos_rating = 0
ratings_soma = 0
ratings_media = 0

count_lines = 0
count_cleaned = 0

filename = "../data/dataset_sort.txt"
cleandataset_filename = "../data/dataset_clean.txt"

# Returns elapsed time acording to the start time
def elapsed(inicio):
	print 'done'
	fim = time.time()
	elapsed = (fim - inicio) / 60
	print 'duracao: %f min' % elapsed

inicio = time.time()
print 'cleaning dataset %s ...' % filename
# TODO: read from a lot of log files
file_cleandataset = open(cleandataset_filename, "w")
for line in fileinput.input(filename):
	count_lines = count_lines + 1
	linha = ''
	try:
		(user, media, rating) = line.split('|')
		rating = rating.strip()
		rating = int(rating.strip())
		linha = '%s|%s|%d' % (user, media, rating)
		file_cleandataset.write(linha+'\n')
		count_cleaned = count_cleaned + 1
		videos_rating = videos_rating + 1
		ratings_soma = ratings_soma + rating
	except 	Exception, why:
		#print 'Erro: %s ' % linha
        # count was not a number, so silently
        # ignore/discard this line
		#print "Passing...", why
		pass
	videos = videos + 1
ratings_media = ratings_soma / videos_rating
file_cleandataset.close()
elapsed(inicio)

print 'Linhasinhas analisadas: %d' % count_lines
print 'Linhas limpas: %d' % count_cleaned
print '*' * 60
print 'videos: %d' % videos
print 'videos com rating: %d' % videos_rating
print 'media ratings: %f' % ratings_media
