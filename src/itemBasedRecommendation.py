#!/usr/bin/python

# Item based recommendation media system

import urllib
from xml.dom import minidom
from similarity import *
from logParser import mediaUserDict

URI = 'http://webmedia-api-live.globoi.com/1.0/video/%s'

def getMediaTitle(midia_id):
	uri = URI % midia_id
	dom = minidom.parse(urllib.urlopen(uri))
	media_node = dom.getElementsByTagName("midia")

	return media_node[0].attributes["titulo"].value


# TODO: dictionary -> matrix NxM
# TODO: SVD


# TEST: Item similarity dataset
mediaDict = calculateSimilarItems(mediaUserDict)

print "838440 - %s" % getMediaTitle(838440)

for similarity, midia_id in mediaDict['838440']:
	print "%s\t%s" % (midia_id, getMediaTitle(int(midia_id)))
