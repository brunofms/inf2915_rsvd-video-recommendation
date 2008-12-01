import sys,os,fileinput
from operator import itemgetter

NETFLIX_PROBE_FILE='../data/netflix/predicted_glb_ml.txt'
#file_netflix = open("../data/netflix/dataset.txt", "w")
videos = {}
midia = 'a'
i = 0
for line in fileinput.input(NETFLIX_PROBE_FILE):
	try:
		if line.endswith(':\n'):
			line = line.strip()
			x = line.find(':')
			midia = line[:x]
			midia = int(midia)
			videos[midia] = []
			#print midia
		else:
			predicted = line.strip()
			videos[midia].append(predicted)
			#print '%s\t%s' % (user, midia)
	except Exception, why:
		print why
		pass
		


for key in sorted(videos.iterkeys()):
	print "%s:" % (key)
	lista_aux = videos[key]
	for item in lista_aux:
		print item	

