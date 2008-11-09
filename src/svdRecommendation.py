#!/usr/bin/python

# Item based recommendation media system

import similarity
from operator import itemgetter
from logParserSvd import mediaUserDict
from logParserSvd import user2count
from logParserSvd import video2count

print 'Total de videos vistos: %s' % len(video2count)
print 'Total de usuarios: %s' % len(user2count)

var_file = open("dicionario_media.txt", "w")
var_file.write(str(mediaUserDict))
var_file.close();

var_file = open("user2count.txt", "w")
var_file.write(str(user2count))
var_file.close();

var_file = open("video2count.txt", "w")
var_file.write(str(video2count))
var_file.close();

print 'arquivo com o dicionario escrito'

#print similarity.topMatches(mediaUserDict, '904968', 10, similarity.sim_distance)


#print '-' * 50
#print mediaUserDict
#print '-' * 50


matriz = similarity.getArrayFromDict(mediaUserDict)
u, sigma, q = similarity.svd_components(matriz)

print 'u:\n%s\n' % u
print 'eigen value:\n%s\n' % sigma
print 'q transposta:\n%s\n' % q
print '*' * 50