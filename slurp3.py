from error_model import error_model_prob

import re, collections


# format the corpus as a list of lowercase words
def features(text):
	return re.findall('[a-z]+', text.lower())

# produce a word -> count mapping structure
def train(features):
	BAG_OF_WORDS = collections.defaultdict(lambda: 1)
	for f in features:
		BAG_OF_WORDS[f] += 1
	return BAG_OF_WORDS

BAG_OF_WORDS = train(features(open('big.txt').read()))
CHAR_SET = 'abcdefghijklmnopqrstuvwxyz'

# filter a set of words so that they're all English words (in our corpus)
def known(word):
	return word in BAG_OF_WORDS


def edits1(word):
	splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
	inserts = [('ins', a[-1] + c, a[1:] + c + b) for a, b in map(lambda e: ('@' + e[0], e[1]), splits) for c in CHAR_SET]
	deletes = [('del', a[-1] + b[0], a[1:] + b[1:]) for a, b in map(lambda e: ('@' + e[0], e[1]), splits) if b]
	substitutions = [('sub', b[0] + c, a + c + b[1:]) for a, b in splits for c in CHAR_SET if b]
	transposes = [('trans', b[0] + b[1], a + b[1] + b[0] + b[2:]) for a, b in splits if len(b) > 1]
	return set(deletes + transposes + substitutions + inserts)

def edits(word, dist):
	if dist == 1:
		return edits1(word)
	return set((operation, confusion_params, e) for operation, confusion_params, generated_word in edits(word, dist - 1) for e in edits1(generated_word))

def language_model_prob(word):
	total = 0
	count = 0
	for k, v in BAG_OF_WORDS.items():
		total += v
		if word == k:
			count = v
	return float(count) / total

def correct(word):
	candidates = edits(word, 1) or edits(word, 2)
	print len(candidates)
	w = ("", 0)
	for c in candidates:
		candidate = c[2] if isinstance(c[2], str) else c[2][2]
		best_word, best_prob = w
		curr_prob = error_model_prob(c) * language_model_prob(candidate)
		if  curr_prob > best_prob and known(candidate):
			w = (candidate, curr_prob)
	return w

print 'corrected word params:' + str(correct('coww'))