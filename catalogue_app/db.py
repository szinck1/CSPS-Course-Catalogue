import os
from flask import g
import mysql.connector
from catalogue_app.config import Config


# Origin query count, excluding 'Selection' page: 106!!!
ctr = 0
def query_mysql(query, args=None, dict_=False):
	"""Execute query on connection stored in g."""
	cnx = get_db(local=Config.LOCAL_DB)
	cursor = cnx.cursor(dictionary=dict_)
	cursor.execute(query, args)
	results = cursor.fetchall()
	cursor.close()
	
	# Temporary code to track number of queries
	#global ctr
	#ctr += 1
	#print('{0}: {1}'.format(ctr, query))
	
	return results


def get_db(local):
	"""Connect to db and store connection in g for
	life of request.
	"""
	if 'db2' not in g:
		if local:
			g.db2 = mysql.connector.connect(host='localhost',
											user='admin',
											password='Newton11',
											database='csps_dashboards')
		else:
			g.db2 = mysql.connector.connect(host=os.environ.get('DB_HOST'),
											user=os.environ.get('DB_USER'),
											password=os.environ.get('DB_PASSWORD'),
											database=os.environ.get('DB_DATABASE_NAME'))
	return g.db2


def close_db(e=None):
	"""Remove connection to db from g and close."""
	db2 = g.pop('db2', None)
	if db2 is not None:
		db2.close()


def init_app(app):
	"""In factory function, register the close_db function so
	that connections closed at end of request.
	"""
	app.teardown_appcontext(close_db)
