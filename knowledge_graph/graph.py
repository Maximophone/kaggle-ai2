import sqlite3
import utils
from nodes import NodeFactory

_FACTORY = NodeFactory()

class Graph(object):
	def __init__(self,db_file):
		self.db_file = db_file
		self.concepts = _FACTORY.nodes
		self.concept_names = _FACTORY.concept_names
		self.statements = _FACTORY.statements
		self.concepts_to_uid = _FACTORY.concepts_to_uid

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

	def _add_concept(self,concept):
		sql = """
		INSERT INTO concepts (concept)
		VALUES ('{concept}')
		""".format(concept=concept)
		uid = utils.execute_sql(self.db_file,sql)
		if not self.concepts.has_key(uid): _FACTORY.new_node(uid,concept)
		return uid

	def _add_relation(self,statement):
		luid = statement[0][0]
		ruid = statement[1][0]
		riuid = statement[2][0]
		lc = statement[0][1]
		r = statement[1][1]
		ric = statement[2][1]
		sql = """
		INSERT INTO statements (left_UID,left_concept,relation_UID,relation,right_UID,right_concept)
		VALUES ({left_uid},'{left_concept}',{relation_uid},'{relation}',{right_uid},'{right_concept}')
		""".format(left_uid=luid,left_concept=lc,relation_uid=ruid,relation=r,right_uid=riuid,right_concept=ric)
		utils.execute_sql(self.db_file,sql)
		_FACTORY.add_relation(luid,ruid,riuid)

	def _check_exists(self,statement):
		return statement in self.statements

	def _get_concept_uid(self,concept):
		return self.concepts_to_uid[concept]

	def add_knowledge(self,statement):
		if self._check_exists(statement): return
		if statement[0] not in self.concept_names:
			left_uid = self._add_concept(statement[0])
		else:
			left_uid = self._get_concept_uid(statement[0])
		if statement[1] not in self.concept_names:
			relation_uid = self._add_concept(statement[1])
		else:
			relation_uid = self._get_concept_uid(statement[1])
		if statement[2] not in self.concept_names:
			right_uid = self._add_concept(statement[2])
		else:
			right_uid = self._get_concept_uid(statement[2])
		self._add_relation(((left_uid,statement[0]),(relation_uid,statement[1]),(right_uid,statement[2])))

	def add_knowledge_from_file(self,file_name):
		statements = utils.parse_knowledge_file(file_name)
		for statement in statements:
			self.add_knowledge(statement)