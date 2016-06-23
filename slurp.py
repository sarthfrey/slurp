import re
import collections


def features(text):
	return re.findall('[a-z-\']+', text.lower())

def train(features):
	bag_of_words = collections.defaultdict(lambda: 1)
	for f in features:
		bag_of_words[f] += 1
	return bag_of_words

bag_of_words = train(features(open('big.txt').read()))
char_set = 'abcdefghijklmnopqrstuvwxyz-\''

def edits1(word):
	splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
	deletes = [(a + b[1:], a[-1] + b[0], "del") for a, b in map(lambda e: ('@' + e[0], e[1]), splits) if b]
	transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
	replaces = [a + c + b[1:] for a, b in splits for c in char_set if b]
	inserts = [a + c + b for a, b in map(lambda e: ('@' + e[0], e[1]), splits) for c in char_set]
	return set(deletes + transposes + replaces + inserts)

def edits2(word):
	return set(e2 for e1 in edits1(word) for e2 in edits1(e1))

def known_edits2(word):
	return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in bag_of_words )

def known(words):
	return set(w for w in words if w in bag_of_words)

def correct(word):
	candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
	return max(candidates, key=bag_of_words.get)

