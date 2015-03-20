# including libraries
import traceback
from HTMLParser import HTMLParser
import argparse
import sys
import urllib2
import sys
from api.getKeywords import HTMLTokenizer

# Begin parsing the arguments:
# We provide 3 modes for input
# 1. url
# 2. string
# 3. file path

description = """HTML Schema Detector"""
parser = argparse.ArgumentParser(description=description)

parser.add_argument(
	"-t", "--type", metavar="TYPE", dest="type", type=str,
	choices=['url','path','string'],
	help="Specify if following argument is url, file path, or string", required=True
)


opts = parser.parse_args()
ip_type = opts.type

# In this function, we process the arguments to obtain actual input
def getInput(ip_type,):
	if ip_type == "url":
		try:
			print "URL: "
			path = raw_input()
			print "Connecting to " + path
			html = urllib2.urlopen(path).read()
			print "Data Successfully Received."
			return html
		except e:
			print "URL unreachable."
			print str(e)
			exit()
	elif ip_type == "path":
		try:
			print "File Path: "
			path = raw_input()
			fo = open("foo.txt", "r")
			return fo.read()
		except:
			print "File cannot be opened."
			exit()
	else:
		print "String: "
		path = raw_input()
		return path


ip = getInput(ip_type)
tokenizer = HTMLTokenizer()
tokenizer.feed(ip)
tokenizer.tokenize()
tokenizer.keep_one_stem()
tokenizer.pos_tag()
tokenizer.rm_stopwords()
print tokenizer.token_list
