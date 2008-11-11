#!/usr/bin/python

# Item based recommendation media system

import sys
import os
import time
import similarity
from operator import itemgetter
from logParserSvd import mediaUserDict
from logParserSvd import user2count
from logParserSvd import video2count
from logParserSvd import media_matrix
from logParserSvd import user_index
from logParserSvd import video_index

def elapsed(inicio):
	print 'done'
	fim = time.time()
	elapsed = (fim - inicio) / 60
	print 'duracao: %f min' % elapsed
	
	



print 'Total de videos vistos: %s' % len(video2count)
print 'Total de usuarios: %s' % len(user2count)

#var_file = open("dicionario_media.txt", "w")
#var_file.write(str(mediaUserDict))
#var_file.close();

print 'escrevendo user2count.txt'
var_file = open("user2count.txt", "w")
var_file.write(str(user2count))
var_file.close();
print 'done'
print 'escrevendo video2count.txt'
var_file = open("video2count.txt", "w")
var_file.write(str(video2count))
var_file.close();
print 'done'
#Sorted
var_file = open("user2count_sorted.txt", "w")
var_file.write(str(similarity.getSortedDict(user2count)))
var_file.close();

var_file = open("video2count_sorted.txt", "w")
var_file.write(str(similarity.getSortedDict(video2count)))
var_file.close();


#print similarity.topMatches(mediaUserDict, '904968', 10, similarity.sim_distance)


#print '-' * 50
#print mediaUserDict
#print '-' * 50


#var_file = open("matriz.txt", "w")
#var_file.write(str(matriz))
#var_file.close();

size_linha = len(media_matrix[0])
print 'total de linhas: %d' % len(media_matrix)
print 'tamanho da linha 0: %d' % size_linha
print 'tamanho da linha 1: %d' % len(media_matrix[1])
print 'tamanho da linha 2: %d' % len(media_matrix[2])
print 'tamanho da linha 3: %d' % len(media_matrix[3])


print 'obtendo as componentes svd...'
inicio = time.time()
u, sigma, q = similarity.svd_components(media_matrix)

elapsed(inicio)

print 'u:\n%s\n' % u
print 'eigen value:\n%s\n' % sigma
print 'q transposta:\n%s\n' % q
print '*' * 50

