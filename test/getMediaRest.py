import urllib
from xml.dom import minidom

URI = 'http://webmedia-api-live.globoi.com/1.0/video/%s'

def getMediaAverageRating(midia_id):
	uri = URI % midia_id
	dom = minidom.parse(urllib.urlopen(uri))
	media_node = dom.getElementsByTagName("avaliacao")

#	for node in media_node[0]:
	soma = media_node[0].attributes["somaVotos"].value
	qde = media_node[0].attributes["quantidadeVotos"].value

	return float(soma)/float(qde)


print "%f" % (getMediaAverageRating(838440))
