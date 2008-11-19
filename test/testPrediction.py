from math import *

# test dataset file path
TEST_DATASET_FILE='../data/dataset_teste.txt'

# Returns the RMSE of the proposed train process
def testData(w,q): 
	i=0
    # le o dataset de testes
	for line in fileinput.input(TEST_DATASET_FILE):
		try:
			line.strip()
			user,media,rating = line.split('\t')
			user = user.strip()
			media = media.strip()
			rating = int(rating.strip())

			if w.has_key(user) and q.has_key(media):
				predicted = int(w[user]*q[media])
				err = err+(rating-predicted)**2
				i += 1

		except Exception, why:
			pass

	mse = err/i
	rmse = sqrt(mse)

	return rmse
