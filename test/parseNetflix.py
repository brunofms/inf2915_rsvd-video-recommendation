import sys,os,fileinput

NETFLIX_DATASET_DIR='/Volumes/Untitled/machine_learning/netflix/download/training_set/'
#file_netflix = open("../data/netflix/dataset.txt", "w")

for file_item in os.listdir(NETFLIX_DATASET_DIR):
	filename = '%s/%s' % (NETFLIX_DATASET_DIR, file_item)

	i = 0
	for line in fileinput.input(filename):
		i = i + 1
		try:
			if i == 1:
				end=line.find(':')
				midia_id=line[0:end]
			else:
				user,rating,date=line.split(',')
				print "%s\t%s\t%s" % (user, midia_id, rating)
		except Exception, why:
			print why
			pass
