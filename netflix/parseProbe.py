import sys,os,fileinput

NETFLIX_PROBE_FILE='../data/netflix/qualifying.txt'
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
			(user, data) = line.split(',')
			user = user.strip()
			print '%s\t%s' % (user, midia)
	except Exception, why:
		print why
		pass

'''
for keys in videos.keys():
	j = len(keys)
	if j == 1:
		print '000000%s' % keys
	elif j == 2:
		print '00000%s' % keys
	elif j == 3:
		print '0000%s' % keys
	elif j == 4:
		print '000%s' % keys
	elif j == 5:
		print '00%s' % keys
	elif j == 6:
		print '0%s' % keys
	else:
		print '%s' % keys
'''