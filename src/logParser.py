#!/usr/bin/python

from collections import defaultdict 
import sys, hashlib, fileinput, os

# Returns the main fields from an apache access log file
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

	#parse path
	patt = re.compile('(.*)\?')
	mobj = patt.search(request)
	output['file_path'] = mobj.group(1)

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

# Returns the file size of a given media
def getMediaFileSize (path):
	# TODO: put on config file
	mount = '/mnt/filer_producao/flashvideo'
	file_path = mount + path

	return os.path.getsize(file_path)

# Create media : user : rate dictionary -> Item centric!
# video = { usuario:gosto, usuario:gosto ... }
mediaUserDict = defaultdict(dict)

# TODO: read from a lot of log files
for line in fileinput.input("../data/logs_flashvideo/access.Nov022008.riols29"):
	try:
		# TODO: instead of IP + User agent, use only urchin.js utma field
		# TODO: 'tripao' code nomore! Use REGEXP 
		result = parseLog(line)

		# retrieving info
		user = hashlib.md5(result['ip_address'] + result['user_agent']).hexdigest().strip()
		media = result['midia_id'].strip()
		downloaded = float(result['return_byte'].strip())
		size = float(getMediaFileSize(result['file_path']))

		view_rate = downloaded/size

		# re-generated video adds noise to the dataset
		if view_rate <= 1:
			# how much have been downloaded
			mediaUserDict[media][user] = view_rate

	except 	Exception, why:
        # count was not a number, so silently
        # ignore/discard this line
		#print "Passing...", why
		pass
