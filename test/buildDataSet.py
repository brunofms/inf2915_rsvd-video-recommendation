#!/usr/bin/python

# Bruno de F. Melo e Souza
# Gustavo Soares Souza
# Project DataSet Builder

import time
from collections import defaultdict
from operator import itemgetter
import sys, hashlib, fileinput, os

#201.19.101.6 - - [02/Nov/2008:23:57:41 -0200] "GET /esporte/1/tempo_real/2008/11/02/EFWEBRA_T_905549_flvbl.flv?0312256775751206325916122567745660291106865I+d/Qvah6yPmW2Y7MbsCg HTTP/1.1" 200 14218153 "http://video.globo.com/Portal/videos/cda/player/player.swf" "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506; InfoPath.2)" "RMID=bd195dd4489df250; __utma=156749805.1050736587.1218310759.1224084396.1225677441.10; __utmz=156749805.1225677441.10.5.utmccn=(referral)|utmcsr=globoesporte.globo.com|utmcct=/Esportes/Noticias/Futebol/Brasileirao/Serie_A/0,,MUL846435-9827,00.html|utmcmd=referral; __utmb=156749805; __utmc=156749805"i - 138
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
	
	#get __utma=
	#patt = re.compile('__utma=(.*)[^ ];')
	#mobj = patt.search(rest)
	#output['utma'] = mobj.group(1)
	#print 'rest: %s' % rest
	#print 'utma: %s' % output['utma']
	

	return output

# Returns the file size of a given media
def getMediaFileSize (path):
	# TODO: put on config file
	mount = '/mnt/filer_producao/flashvideo'
	file_path = mount + path

	return os.path.getsize(file_path)

# Returns elapsed time acording to the start time
def elapsed(inicio):
	print 'done'
	fim = time.time()
	elapsed = (fim - inicio) / 60
	print 'duracao: %f min' % elapsed


#################
## MAIN #########
#################
logs_dir = "../data/logs_flashvideo"
filename = "../data/new.log"
file_dataset = "../data/dataset.txt"

inicio = time.time()
dataset_file = open(file_dataset, "w")

files_to_process = os.listdir(logs_dir)
print 'files to process: %s' % files_to_process
for file_item in files_to_process:
	filename = '%s/%s' % (logs_dir, file_item)
	print 'reading and parsing file %s ...' % filename
	# TODO: read from a lot of log files
	for line in fileinput.input(filename):
		try:
			# TODO: instead of IP + User agent, use only urchin.js utma field
			# TODO: 'tripao' code nomore! Use REGEXP 
			result = parseLog(line)

			# retrieving info
			user = hashlib.md5(result['ip_address'] + result['user_agent']).hexdigest().strip()
			media = result['midia_id'].strip()
			#downloaded = float(result['return_byte'].strip())
			#size = float(getMediaFileSize(result['file_path']))

			#view_rate = downloaded/size
			view_rate = 1

			# re-generated video adds noise to the dataset
			if view_rate <= 1:
				# how much have been downloaded
				#mediaUserDict[media][user] = view_rate
				dataset_file.write('%s\t%s\n' % (user, media))
				mediaUserDict[user][media] = view_rate
				user2count[user] = user2count.get(user, 0) + 1
				video2count[media] = (video2count.get(media, 0)) + 1
		
			count_lines = count_lines + 1

		except 	Exception, why:
	        # count was not a number, so silently
	        # ignore/discard this line
			#print "Passing...", why
			pass

dataset_file.close()
elapsed(inicio)
print 'total de linhas processadas: %d' % count_lines
