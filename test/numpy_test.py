from numpy.linalg import *
from numpy import *
from operator import itemgetter

users = { 1 : "Ben", 2 : "Tom", 3 : "John", 4 : "Fred" }
a = array([[5,5,0,5],
           [5,0,3,4],
           [3,4,0,3],
           [0,0,5,3],
           [5,4,4,5],
           [5,4,5,5]])

print 'matriz a: \n%s\n' % a


u,sigma,vh = svd(a, full_matrices = 1, compute_uv = 1)
vh = transpose(vh)
#sigma = diag(sigma)


print 'u:\n%s\n' % u
print 'sigma:\n%s\n' % sigma
print 'vh transposta:\n%s\n' % vh


#primeira e segunda coluna de u 
u2 = u[:,:2]
num_linhas_u2 = size(u2,0)
print 'u2:\n%s\n' % u2


#primeira e segunda coluna de vh_t
vh2 = vh[:,:2]
num_linhas_vh2 = size(vh2,0)
print 'vh2:\n%s\n' % vh2

#dois primeiros autovalores
#autovalores = eigvals(sigma)
autovalores = diag(sigma[0:2])

print 'autovalores:\n%s\n' % autovalores
inversa_autovalores = inv(autovalores)
print 'inversa:'
print inversa_autovalores


bob = array([5,5,0,0,0,5])
print '\nhere comes bob:\n%s\n' % bob

bobembed = mat(bob) * mat(u2) * mat(inversa_autovalores)
print 'bobembed:\n%s\n' % bobembed

#calcula similaridade do coseno e cada usuario da matriz u2
user_sim= {}
count = 1
for row in xrange(num_linhas_vh2):
	x = vh2[row,:]
	#print 'linha %d -> %s' % (row,x)
	x_t = transpose(x)
	bobembed_t = transpose(bobembed)
	#print 'x_t:\n%s\n' % x_t
	#print 'bobembed_t:\n%s\n' % bobembed_t
	dot_product = dot(mat(x_t),mat(bobembed_t))
	numerador = norm(dot_product)
	#print '\tnumerador: %f' % numerador
	denominador = norm(x) * norm(bobembed)
	#print '\tdenominador: %f' % denominador
	coseno = numerador / denominador
	#print '\tcoseno: %f' % coseno
	user_sim[count] = coseno
	count = count + 1
	
#print 'similaridade com os usuarios:'
#print user_sim
print '-' * 60
print 'list ordenada por similaridade com os usuarios:'
print sorted(user_sim.items(), key=itemgetter(1), reverse=True)
print '-' * 60