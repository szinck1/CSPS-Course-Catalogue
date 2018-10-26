import mysql.connector
from wtforms import Form, SelectField
from configparser import ConfigParser

# Get config vals for MySQL
parser = ConfigParser()
parser.read('./mysql_info/mysql_config.cfg')


# Internal function to query data from MySQL
def _query_mysql(query, all=True):
	cnx = mysql.connector.connect(user=parser.get('db', 'user'),
								  password=parser.get('db', 'password'),
								  host=parser.get('db', 'host'),
								  database=parser.get('db', 'database'))
	cursor = cnx.cursor()
	cursor.execute(query)
	results = cursor.fetchall() if all else cursor.fetchone()
	cnx.close()
	return results


query = ("SELECT DISTINCT course_title FROM lsr2018 ORDER BY 1 ASC;")
results = _query_mysql(query)
# SelectField takes a list of tuples
course_titles = [(val, val) for tup in results for val in tup]


class CourseForm(Form):
	course_title = SelectField('Course Title', choices=course_titles)
