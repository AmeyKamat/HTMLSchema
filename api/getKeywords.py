import nltk
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from HTMLParser import HTMLParser

class HTMLTokenizer(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.token_list = []
		self.string = ""
		self.stem_list = []
		
	def handle_starttag(self, tag, attrs):
		self.lasttag = tag;

	def handle_data(self,data):
		if(self.lasttag != 'script' and self.lasttag != 'style'):
			self.string = self.string + " " + str(data)
	
	def tokenize(self):
		self.token_list = nltk.word_tokenize(self.string)
		self.token_list=list(set(self.token_list))
		
	def pos_tag(self):
		self.token_list = nltk.pos_tag(self.token_list)
		
	
	def keep_one_stem(self):
		temp = []
		self.token_list = [token.decode("utf-8") for token in self.token_list]
		stemmer = SnowballStemmer("english")
		self.stem_list = [stemmer.stem(token) for token in self.token_list]
		self.stem_list=list(set(self.stem_list))
		for token in self.token_list:
			if stemmer.stem(token) in self.stem_list:
				temp.append(token)
				self.stem_list.remove(stemmer.stem(token))
		self.token_list = temp
		self.stem_list = [stemmer.stem(token) for token in self.token_list]

	def rm_stopwords(self):
		stop = stopwords.words('english')
		self.token_list = [token for token in self.token_list if token[0].lower() not in stop]
