# we include all libraries here
from HTMLParser import HTMLParser
import urllib2
import re

# Definations of frequently used variable
url = "http://www.w3schools.com/tags/"
urlList = []
compTable = []
flag =0

# create a subclass and override the handler methods
class MainHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
		self.lastTag = tag
		for name, value in attrs:
			if name == 'class':
				self.lastClass = value
				if tag == 'table':
					self.lastTableClass = value
			else:
				self.lastClass = ""
		if(tag == 'a' and flag ==0):
			for i in range(0,len(attrs)):
				if (attrs[i][0] == 'href' and "tag_" in attrs[i][1]):
					if ("://" in attrs[i][1]):
						if(attrs[i][1] not in urlList):
							urlList.append(attrs[i][1])
					else:
						if((url + attrs[i][1]) not in urlList):
							urlList.append(url + attrs[i][1])

    def handle_endtag(self, tag):
        pass
    def handle_data(self, data):
		global compTable
		if flag==1 and (self.lastTag == 'td' or (self.lastTag == 'span' and self.lastClass == 'deprecated')) and self.lastTableClass=='browserref notranslate':
			value = parseTag(data)
			if value != None:
				compTable.append(value)


	
def parseTag(data):
	if re.match(r'^[0-9]+\.[0-9]+$', data) or re.match(r'^Yes$', data) or re.match(r'^Not supported$', data) or re.match(r'^[0-9]+$', data):
		return data

def buildJSON():
	i=2
	attempt = 1
	print "Collecting data..."
	global compTable
	repeat = []
	length = len(urlList) 
	while i<length:
		tag = urlList[i][urlList[i].index('_')+1:urlList[i].index('.asp')]
		print "Attempt " + str(attempt) + " : Fetchning data for tag " + tag
		try:
			tag_ref = urllib2.urlopen(urlList[i]).read()
			attempt = 1
		except Exception:
			if(attempt!=4):
				print "Fetching of data unsuccessful for tag " + tag + ". Reattempting fetch..."
				attempt = attempt+1
				continue
			else:
				print "ERROR: All attempts of fetching failed. Terminating the program" 
				exit(0)
		parser.feed(tag_ref)
		print tag + " : " + str(compTable) + " : " + str(i) + " : " + str(i<length) + " : " + str(length)
		compTable = []
		i = i+1

# read from http request
try:
    print "Connecting to w3schools..."
    html = urllib2.urlopen(url).read()
    print "Data Successfully Received."
except Exception:
    print "ERROR: Error in fetching data from w3schools. "
    exit(0)
    
# instantiate the parser and fed it some HTML
parser = MainHTMLParser()
parser.feed(html)
flag =1
buildJSON();
