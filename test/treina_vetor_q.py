#!/usr/local/bin/python

# Bruno de F. Melo e Souza
# Gustavo Soares Souza
# Project Parser

import time
from collections import defaultdict
from operator import itemgetter
import sys, fileinput, os
from svd_impl import *

import pdb
#pdb.set_trace()
########################
## BEGING TRAINING #####
########################
svd_log = open("svd_q.log", "w")
print 'Traingin SVD...'


##################
## VETOR Q #######
##################
inicio = time.time()
print 'obtendo o vetor q...'
q_log = open("vetor_q.log", "w")

err = 0
for j_aux in range(j):
	svd_log.write('q[%d] antes: %f\n' % (j_aux, q[j_aux]))
	for i_aux in range(i):
		Aij = 0
		try:
			Aij = midia_matrix[i_aux][j_aux]
		except Exception:
			pass
		#print 'midia_matrix[i_aux][j_aux]: %f' % Aij
		#print 'erro antes: %f' % err
		err = err + (Aij - (q[j_aux] * w[i_aux])) * w[i_aux]
		#print 'erro depois: %f' % err
	q[j_aux] = q[j_aux] + (lrate * err)
	svd_log.write('q[%d] depois: %f\n' % (j_aux, q[j_aux]))
	err = 0

elapsed(inicio)

print '*' * 60
q_log.write('q: \n%s\n' % q)
q_log.close()

svd_log.close()