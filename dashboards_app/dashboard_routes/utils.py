from configparser import ConfigParser
import mysql.connector

# Get config vals for MySQL
parser = ConfigParser()
parser.read('./dashboards_app/mysql_config.cfg')


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


# Convert SQL datatype Decimal to Python float
def decimal_to_float(my_val):
	return float(str(my_val[0][0]))

# Convert SQL datatype Decimal to percentage for Highcharts
def decimal_to_percent(my_val):
	return round(float(str(my_val[0][0])), 2) * 100

# Convert SQL datatype Decimal to Python int
def decimal_to_int(my_val):
	return int(decimal_to_float(my_val))
