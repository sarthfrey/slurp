import re, collections, json, os

# format the corpus as a list of lowercase words
def features(text):
	return re.findall('[a-z]+', text.lower())

# produce a word -> count mapping structure
def train(features):
	for f in features:
		BAG_OF_WORDS[f] += 1
	return BAG_OF_WORDS

BAG_OF_WORDS = collections.defaultdict(lambda: 1)
 
for file_name in os.listdir('text'):
     f = open(os.path.join('text', file_name), 'r')
     BAG_OF_WORDS = train(features(f.read()))

with open('unigram.json', 'w') as f:
	json.dump(BAG_OF_WORDS, f)