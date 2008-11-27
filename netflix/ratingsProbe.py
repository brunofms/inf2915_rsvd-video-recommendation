import sys,os,fileinput
from collections import defaultdict

NETFLIX_PROBE_FILE='/Users/gustavosoares/repos/git/video-recommendation/data/netflix/probe_parsed.txt'
NETFLIX_DATASET_FILE='/Users/gustavosoares/repos/git/video-recommendation/data/netflix/dataset.txt'
#file_netflix = open("../data/netflix/dataset.txt", "w")

mediaUserDict = defaultdict(dict)

print 'colocando probe.txt na memoria'
for line in fileinput.input(NETFLIX_PROBE_FILE):
		try:
				line = line.strip()
				user, midia = line.split('|')
				user = user.strip()
				midia = midia.strip()
				mediaUserDict[user][midia] = 0
		except Exception, why:
				print 'Erro: ' + why
				pass

print 'done'
print 'obtendo os ratings'

for line in fileinput.input(NETFLIX_DATASET_FILE):
		try:
				line = line.strip()
				user, midia, rating = line.split()
				user = user.strip()
				midia = midia.strip()
				rating = rating.strip()
				if mediaUserDict[user].has_key(midia):
						mediaUserDict[user][midia] = rating
		except Exception, why:
				print 'Erro: %s' % why
				pass

print 'done'

for user_item in mediaUserDict.keys():
	for video_item in mediaUserDict[user_item].keys():
		print '%s\t%s\t%s\n' % (user_item, video_item, mediaUserDict[user_item][video_item])
