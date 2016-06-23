from ast import literal_eval


with open('confusion/ins.data') as f:
	d_ins =  literal_eval(f.read())

with open('confusion/del.data') as f:
	d_del =  literal_eval(f.read())

with open('confusion/sub.data') as f:
	d_sub =  literal_eval(f.read())

with open('confusion/trans.data') as f:
	d_trans =  literal_eval(f.read())

char_set = 'abcdefghijklmnopqrstuvwxyz-\''

def edits1(word):
	splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
	inserts = [('ins', a[-1] + c, a[1:] + c + b) for a, b in map(lambda e: ('@' + e[0], e[1]), splits) for c in char_set]
	deletes = [('del', a[-1] + b[0], a[1:] + b[1:]) for a, b in map(lambda e: ('@' + e[0], e[1]), splits) if b]
	substitutions = [('sub', b[0] + c, a + c + b[1:]) for a, b in splits for c in char_set if b]
	transposes = [('trans', b[0] + b[1], a + b[1] + b[0] + b[2:]) for a, b in splits if len(b) > 1]
	return set(deletes + transposes + substitutions + inserts)

def edits2(word):
	return set(e2 for operation, confusion_params, generated_word in edits1(word) for e2 in edits1(generated_word))

