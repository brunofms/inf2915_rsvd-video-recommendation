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
svd_log = open("svd_w.log", "w")
print 'SVD running...'

##################
## VETOR W #######
##################
inicio = time.time()
print 'obtendo o vetor w...'
w_log = open("vetor_w.log", "w")
err = 0
for i_aux in range(i):
	svd_log.write('w[%d] antes: %f\n' % (i_aux, w[i_aux]))
	for j_aux in range(j):
		'''print 'j_aux: %d' % j_aux
		print 'q[j_aux]: %f' % q[j_aux]
		print 'i_aux: %d' % i_aux
		print 'w[i_aux]: %f' % w[i_aux]'''
		Aij = 0
		try:
			Aij = midia_matrix[i_aux][j_aux]
		except Exception:
			pass
		#print 'midia_matrix[i_aux][j_aux]: %f' % Aij
		#print 'erro antes: %f' % err
		err = err + (Aij - (q[j_aux] * w[i_aux])) * q[j_aux]
		#print 'erro depois: %f' % err
	w[i_aux] = w[i_aux] + (lrate * err)
	svd_log.write('w[%d] depois: %f\n' % (i_aux, w[i_aux]))
	err = 0

elapsed(inicio)

print '*' * 60
w_log.write('w: \n%s\n' % w)
w_log.close()