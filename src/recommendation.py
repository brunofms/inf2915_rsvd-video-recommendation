# Give recommendations using the item similarity dictionary
# without going through the whole dataset
def getRecommendedItems(mediaUserDict, itemMatch, user):
	# TODO: rollback to user-centric dictionary
	userViewedMedia=userMediaDict[user]
	scores={}
	totalSim={}

	# Loop over items viewed by this user
	for (item, download_rate) in userViewedMedia.items():

		# Loop over items similar to this one
		for (similarity, item2) in itemMatch[item]:

			# Ignore if this user has already viewed this item
			if item2 in userViewedMedia: continue

			# Weighted sum of downloaded times similarity
			scores.setdefault(item2,0)
			scores[item2]+=similarity*download_rate

			# Sum of all the similarities
			totalSim.setdefault(item2,0)
			totalSim[item2]+=similarity

		# Divide each total score by total weighting to get an average
		rankings=[(score/totalSim[item], item) for item,score in scores.item()]

		# Return the rankings from highest to lowest
		rankings.sort()
		rankings.reverse()
		return rankings
