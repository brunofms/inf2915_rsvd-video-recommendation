# test dataset file path
TEST_DATASET_FILE=''

# w*q
predicted_ratings=

# Returns the RMSE of the proposed train process
def testData()
	i=0
    # le o dataset de testes
	for line in fileinput.input(TEST_DATASET_FILE):
		try:
			line.strip()
			user, media, rating = line.split('\t')
			user = user.strip()
			media = media.strip()
			rating = int(rating.strip())

			if predicted_ratings.has_key(user) and predicted_ratings[user].has_key(media):
				predicted=int(predicted_ratings[user][media].strip)
				err+=(rating-predicted)**2
				i++

		except Exception, why:
			pass

	mse=err/i
	rmse=sqrt(mse)

	return rmse
