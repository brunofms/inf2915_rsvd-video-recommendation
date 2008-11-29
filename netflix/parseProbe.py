import sys,os,fileinput

NETFLIX_PROBE_FILE='../data/netflix/probe.txt'
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
			videos[midia] = 1
			#print midia
		else:
			user = line.strip()
			print '%s\t%s' % (user, midia)
	except Exception, why:
		print why
		pass

#for keys in videos.keys():
#	print keys