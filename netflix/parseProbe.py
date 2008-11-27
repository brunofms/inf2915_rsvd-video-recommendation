import sys,os,fileinput

NETFLIX_PROBE_FILE='/Users/gustavosoares/repos/git/video-recommendation/data/netflix/probe.txt'
#file_netflix = open("../data/netflix/dataset.txt", "w")

i = 0
for line in fileinput.input(NETFLIX_PROBE_FILE):
	i = i + 1
	try:
		if line.endswith(':\n'):
			line = line.strip()
			x = line.find(':')
			user = line[:x]
		else:
			midia = line.strip()
			print '%s|%s' % (user, midia)
	except Exception, why:
		print why
		pass
