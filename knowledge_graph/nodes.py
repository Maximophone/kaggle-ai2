class NodeFactory(object):
	def __init__(self):
		self.nodes = {}
		self.concept_names = []
		self.statements = []
		self.concepts_to_uid = {}
	def new_node(self,uid,concept):
		self.concept_names.append(concept)
		self.concepts_to_uid[concept] = uid
		self.nodes[uid] = Node(uid,concept)
		return self.nodes[uid]
	def add_relation(self,left_uid,relation_uid,right_uid):
		self.statements.append((self.nodes[left_uid].concept,self.nodes[relation_uid].concept,self.nodes[right_uid].concept))
		self.nodes[left_uid].add_relation(relation_uid,right_uid)
	def get_relations(self,node_uid):
		relations = self.nodes[node_uid].relations
		return [(self.nodes[r[0]],self.nodes[r[1]]) for r in relations]
	def get_relations_explicit(self,node_uid):
		node = self.nodes[node_uid]
		relations = self.get_relations(node_uid)
		return  [(node.concept,r[0].concept,r[1].concept) for r in relations]

class Node(object):
	def __init__(self,uid,concept):
		self.uid = uid
		self.concept = concept
		self.relations = []
	def add_relation(self,relation_uid,concept_uid):
		self.relations.append((relation_uid,concept_uid))
