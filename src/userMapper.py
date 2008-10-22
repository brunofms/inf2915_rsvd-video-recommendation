#!/usr/bin/python

# Bruno de F. Melo e Souza
# Usage: cat videoplayer_AAAAMMDDHH.log | python userMapper.py

import sys
import hashlib

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
	patt = re.compile('midiaId=([0-9]{1,6})')
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
     
	#parse cookie
	#after_user_ag = after_ref_url[e_quote_user_agent+1:]
	#s_quote_cookie = string.index(after_user_ag,"\"")
	#after_user_ag = after_user_ag[s_quote_cookie+1:]
	#e_quote_cookie = string.index(after_user_ag, "\"")
	#if e_quote_cookie - s_quote_cookie==1:
	#	output['cookie'] = ""
	#else:
	#	output['cookie'] = after_user_ag[:e_quote_cookie]
	
	return output

# start script
#print "IP\tAccess Date\tRequest URI\tDownloaded Bytes\tReferer URI\tUser-agent\tCookie"
#print "User\tMedia"
for line in sys.stdin:
	try:
		result = parseLog(line)
		#for x in result.keys():
		#print result['ip_address'], "\t", result['date_time'], "\t", result['request'], "\t", result['return_byte'], "\t", result['refering_url'], "\t", result['user_agent'], "\t", result['cookie']
		print hashlib.md5(result['ip_address'] + result['user_agent']).hexdigest(), "\t", result['midia_id']
	except:
		pass