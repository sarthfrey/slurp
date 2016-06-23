import json


with open('bigram.json', 'r') as f:
	data = json.load(f)

def cleanse(text):
	text = '<S> ' + text
	return text.split()

def prior(preword, postword):
	total_count = 0
	for post in data[preword]:
		total_count += data[preword][post]
	pre_post_count = data[preword][postword]
	return float(pre_post_count) / total_count

def correct(text):
	text = cleanse(text)

	if not text:
		return None

	for i in xrange(1, len(text)):
		preword = '<S>' if not text[i-1] else text[i-1]
		postword = text[i]
		prior = prior(preword=preword, postword=postword) 


