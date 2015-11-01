

def parse_knowledge(file_name):
	with open(file_name,'rb') as f:
		kstring = f.read()
	lines = kstring.split('\r\n')
	lines = [l.split('#')[0] for l in lines]
	relations = [tuple(l.split('>')) for l in lines]
	return relations
