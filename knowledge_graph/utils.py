import sqlite3
import os

def connect_db(db_name):
	return sqlite3.connect(db_name)

def execute_sql(db_file,sql):
	assert os.path.isfile(db_file), "Database %s does not exist"%db_file
	with sqlite3.connect(db_file) as conn:
		c = conn.cursor()
		c.execute(sql)
		file_entry = c.lastrowid
		conn.commit()
	return file_entry

def select(db_file,sql):
	assert os.path.isfile(db_file), "Database %s does not exist"%db_file
	result = []
	with sqlite3.connect(db_file) as conn:
		c = conn.cursor()
		for row in c.execute(sql):
			result.append(row)
	return result

def parse_knowledge_file(file_name):
	with open(file_name,'rb') as f:
		kstring = f.read()
	lines = kstring.split('\r\n')
	lines = [l.split('#')[0] for l in lines]
	tuples = [tuple(l.split('>')) for l in lines]
	statements = [t for t in tuples if len(t)==3]
	return statements