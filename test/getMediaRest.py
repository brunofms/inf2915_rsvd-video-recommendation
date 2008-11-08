import urllib
from xml.dom import minidom

URI = 'http://webmedia-api-live.globoi.com/1.0/video/%s'

def getMediaTitle(midia_id):
	uri = URI % midia_id
	dom = minidom.parse(urllib.urlopen(uri))
	media_node = dom.getElementsByTagName("midia")

#	for node in media_node[0]:
	print media_node[0].attributes["titulo"].value


getMediaTitle(838440)
