from error_model import error_model_prob

import re, collections, json

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

def known(words):
	return set(w for w in words if w in BAG_OF_WORDS)

def known_word(word):
	return word in BAG_OF_WORDS

def known_edits1(word):
	return set(e for e in edits(word, 1) if e[2] in BAG_OF_WORDS)

def known_edits2(word):
	return set(e for e in edits(word, 2) if e[2][2] in BAG_OF_WORDS)

def language_model_prob(word, total=4052075):
	count = BAG_OF_WORDS[word] + 1
	return float(count) / (total + 1)


def correct(word, bag_of_words, alpha=1, beta=1):
	global BAG_OF_WORDS
	BAG_OF_WORDS = bag_of_words
	candidates = known_edits1(word) or known_edits2(word)
	w = ("", 0)
	for c in candidates:
		candidate = c[2] if isinstance(c[2], str) else c[2][2]
		best_word, best_prob = w
		curr_prob = error_model_prob(c, beta) * language_model_prob(candidate) ** alpha
		if  curr_prob > best_prob and known(candidate):
			w = (candidate, curr_prob)
	return w[0]