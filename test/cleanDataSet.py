#!/usr/local/bin/python

# Bruno de F. Melo e Souza
# Gustavo Soares Souza
# Project Parser

import time
from collections import defaultdict
from operator import itemgetter
import sys, fileinput, os
import pdb


count_lines = 0
count_cleaned = 0

filename = "../data/dataset_treino.txt"
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
	except 	Exception, why:
		#print 'Erro: %s ' % linha
        # count was not a number, so silently
        # ignore/discard this line
		#print "Passing...", why
		pass
file_cleandataset.close()
elapsed(inicio)

print 'Linhasinhas analisadas: %d' % count_lines
print 'Linhas limpas: %d' % count_cleaned
