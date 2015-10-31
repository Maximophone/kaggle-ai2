import sqlite3
import utils
from nodes import NodeFactory

_FACTORY = NodeFactory()

class Graph(object):
	def __init__(self,db_file):
		self.db_file = db_file
		self.concepts = _FACTORY.nodes

	def build_graph(self):
		sql = """SELECT SID,left_UID,left_concept,relation_UID,relation,right_UID,right_concept FROM statements"""
		statements = utils.select(self.db_file,sql)
		for statement in statements:
			sid = statement[0]
			left_uid = statement[1]
			left_concept = statement[2]
			relation_uid = statement[3]
			relation = statement[4]
			right_uid = statement[5]
			right_concept = statement[6]
			if not self.concepts.has_key(left_uid):
				_FACTORY.new_node(left_uid,left_concept)
			if not self.concepts.has_key(relation_uid):
				_FACTORY.new_node(relation_uid,relation)
			if not self.concepts.has_key(right_uid):
				_FACTORY.new_node(right_uid,right_concept)
			_FACTORY.add_relation(left_uid,relation_uid,right_uid)
