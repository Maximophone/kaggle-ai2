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