import sqlite3
from sqlite3 import Error

class db_handling(object):
	def __init__(self):
		self.conn = None
	def db_connection(self):
		try :
			self.conn = sqlite3.connect('network_db.db')
			self.c = self.conn.cursor()
		except Error as e:
			print(e)
	def table_create(self):
		self.c.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='thehosts' ''')
		if self.c.fetchone()[0] == 1:
			print('Table "thehosts " already exist')
		else:
			print('Table "thehosts" created')
			self.c.execute(''' CREATE TABLE thehosts (
						id INTEGER PRIMARY KEY,
						ip_address TEXT NOT NULL, 
						mac_address TEXT NOT NULL,
						mac_vendor TEXT NOT NULL);''')

if __name__ == "__main__":
	D = db_handling()
	D.db_connection()
	D.table_create()