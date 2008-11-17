#!/usr/bin/python

# Bruno de F. Melo e Souza
# Usage: cat ../data/logs_flashvideo/* | grep 200 | python formatDataSet.py > ../data/dataset.txt

from xml.dom import minidom
from collections import defaultdict
import sys
import hashlib
import fileinput
import os
import urllib

URI = 'http://webmedia-api.globoi.com/1.0/video/%s'

FLASHVIDEO_LOGS_DIR = '../data/logs_flashvideo'
RATINGS_FILE = '../data/ratings.txt'

def getMediaAverageRating(midia_id):
	uri = URI % midia_id
	dom = minidom.parse(urllib.urlopen(uri))
	media_node = dom.getElementsByTagName("avaliacao")

	soma = media_node[0].attributes["somaVotos"].value
	qde = media_node[0].attributes["quantidadeVotos"].value

	return float(soma)/float(qde)

def parseLog (input) :
	import re,string
	
	SB    = "["
	EB    = "]"
	IP_SEPR = "- -"

	output = {}

	#clean empty space at the beginning.
	line = string.lstrip(input)
	[ip,rest] = string.split(line,IP_SEPR)
	output['ip_address'] = string.strip(ip)

	#parse the date with the brackets included.
	s_bracket = string.index(rest,SB)
	e_bracket = string.index(rest,EB)
	date_str = string.strip(rest[s_bracket+1:e_bracket])
	output['date_time'] = date_str

	#parse request string to get method, request and protocol.
	current_ind  = e_bracket+1
	request_start = -1
	request_end = -1
	magic_flag = 0

	while current_ind < len(rest):
		if request_start != -1:
			magic_flag = 1
		if rest[current_ind] == "\"" and request_start == -1:
			request_start = current_ind
		if rest[current_ind] == "\"" and request_start != -1 and magic_flag == 1:
			request_end = current_ind

		if request_start >= 0 and request_end >= 0:
			break
		current_ind = current_ind +1

	get_str = string.strip(rest[request_start+1:request_end])
	[method,request,protocol] = string.split(get_str," ")
	output['method']= method
	output['request'] = request
	output['protocol'] = protocol
	
	#parse midia_id
	patt = re.compile('_([0-9]{1,6})_')
	mobj = patt.search(request)
	output['midia_id'] = mobj.group(1)

	#parse return code
	rest = string.strip(rest[request_end+1:])
	ret_code_e_ind = string.index(rest," ")
	ret_code = rest[:ret_code_e_ind]
	output['return_code'] = ret_code

	#parse byte sent
	rest = string.lstrip(rest[ret_code_e_ind+1:])
	byte_sent_e_ind = string.index(rest," ")
	byte_sent = rest[:byte_sent_e_ind]
	output['return_byte'] = byte_sent

	#parse refering url
	after_byte_sent = rest[byte_sent_e_ind+1:]
	s_quote_ref_url = string.index(after_byte_sent,"\"")
	after_byte_sent = after_byte_sent[s_quote_ref_url+1:]
	e_quote_ref_url = string.index(after_byte_sent,"\"")
	if e_quote_ref_url-s_quote_ref_url==1:
		output['refering_url'] = ""
	else:
		output['refering_url'] = after_byte_sent[:e_quote_ref_url]

	#parse user agent
	after_ref_url = after_byte_sent[e_quote_ref_url+1:]
	s_quote_user_agent = string.index(after_ref_url,"\"")
	after_ref_url = after_ref_url[s_quote_user_agent+1:]
	e_quote_user_agent = string.index(after_ref_url,"\"")
	if e_quote_user_agent - s_quote_user_agent==1:
		output['user_agent'] = ""
	else:
		output['user_agent'] = after_ref_url[:e_quote_user_agent]
     
	return output

# MAIN

#
# fulfill ratings dictionary

ratings_dict = defaultdict(dict)

for line in fileinput.input(RATINGS_FILE):
	try:
		line.strip()
		user, media, rating = line.split('\t')
		user = user.strip()
		media = media.strip()
		rating = rating.strip()

		ratings_dict[user][media] = rating
	except Exception, why:
		pass

#
# fulfill user-media dictionary which ratings for viewed videos

for line in sys.stdin:
	try:
		# DEBUG
		#print line

		# Parsing log
		result = parseLog(line)

		# retrieving info
		user = hashlib.md5(result['ip_address'] + result['user_agent']).hexdigest().strip()
		media = result['midia_id'].strip()

		if ratings_dict.has_key(user) and ratings_dict[user].has_key(media):
			rating = ratings_dict[user][media].strip()
		else:
			rating = getMediaAverageRating(media)

		print "%s|%s|%s" % (user, media, rating)

	except Exception, why:
		#print "Passing...", why
		pass
