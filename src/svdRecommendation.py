#!/usr/bin/python

# Item based recommendation media system

import similarity

from logParser import mediaUserDict


print similarity.topMatches(mediaUserDict, '904968', 10, similarity.sim_distance)

var_file = open("dicionario_media.txt", "w")
var_file.write(str(mediaUserDict))
print 'arquivo com o dicionario escrito'
#print '-' * 50
#print mediaUserDict
#print '-' * 50

var_file.close();
matriz = similarity.getArrayFromDict(mediaUserDict)
u, sigma, q = similarity.svd_components(matriz)

print 'u:\n%s\n' % u
print 'eigen value:\n%s\n' % sigma
print 'q transposta:\n%s\n' % q
print '*' * 50