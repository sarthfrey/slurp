from ast import literal_eval


with open('confusion/ins.data') as f:
	d_ins = literal_eval(f.read())

with open('confusion/del.data') as f:
	d_del = literal_eval(f.read())

with open('confusion/sub.data') as f:
	d_sub = literal_eval(f.read())

with open('confusion/trans.data') as f:
	d_trans = literal_eval(f.read())

def edit_prob(operation, confusion_params):
	x = confusion_params[0]
	y = confusion_params[1]
	operation_choice = {
		'ins': d_ins,
		'del': d_del,
		'sub': d_sub,
		'trans': d_trans
	}
	confusion_matrix = operation_choice[operation]
	total = 0
	for k, v in confusion_matrix.items():
		if k[1] == y:
			total += v
		if confusion_params == k:
			count = v
	return float(count) / total

def error_model_prob(candidate_data):
	operation, confusion_params, candidate = candidate_data
	if isinstance(candidate, str):
		return edit_prob(operation, confusion_params)
	return edit_prob(operation, confusion_params) * edit_prob(candidate[0], candidate[1])


