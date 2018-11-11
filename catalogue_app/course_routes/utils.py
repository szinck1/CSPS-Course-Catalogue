from configparser import ConfigParser
import mysql.connector

# Get config vals for MySQL
parser = ConfigParser()
parser.read('./catalogue_app/mysql_config.cfg')


# Query data from MySQL
def query_mysql(query, args=None):
	cnx = mysql.connector.connect(user=parser.get('db', 'user'),
								  password=parser.get('db', 'password'),
								  host=parser.get('db', 'host'),
								  database=parser.get('db', 'database'))
	cursor = cnx.cursor()
	cursor.execute(query, args)
	results = cursor.fetchall()
	cursor.close()
	cnx.close()
	return results


# Helper functions to convert MySQL results to desired dtype
def as_string(my_val):
	return str(my_val[0][0])

def as_float(my_val):
	return float(as_string(my_val))

def as_int(my_val):
	return int(as_float(my_val))

def as_percent(my_val):
	return round(as_float(my_val), 2) * 100
