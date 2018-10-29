from configparser import ConfigParser
import mysql.connector

# Get config vals for MySQL
parser = ConfigParser()
parser.read('./dashboards_app/mysql_info/mysql_config.cfg')


# Query data from MySQL
def query_mysql(query, all=True):
	cnx = mysql.connector.connect(user=parser.get('db', 'user'),
								  password=parser.get('db', 'password'),
								  host=parser.get('db', 'host'),
								  database=parser.get('db', 'database'))
	cursor = cnx.cursor()
	cursor.execute(query)
	results = cursor.fetchall() if all else cursor.fetchone()
	cnx.close()
	return results


# Convert SQL datatype Decimal to Python float
def decimal_to_float(my_val):
	return float(str(my_val[0][0]))


# Convert SQL datatype Decimal to Python int
def decimal_to_int(my_val):
	return int(decimal_to_float(my_val))
