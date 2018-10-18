import mysql.connector
from wtforms import Form, SelectField
from configparser import ConfigParser

# Get config vals for MySQL
parser = ConfigParser()
parser.read('config.cfg')

# Get distinct course titles currently in dataset
query = ("SELECT DISTINCT course_title FROM lsr ORDER BY 1 ASC;")
cnx = mysql.connector.connect(user=parser.get('db', 'user'),
							  password=parser.get('db', 'password'),
							  host=parser.get('db', 'host'),
							  database=parser.get('db', 'database'))
cursor = cnx.cursor()
cursor.execute(query)
results = cursor.fetchall()
cnx.close()
# SelectField takes a list of tuples
course_titles = [(val, val) for tup in results for val in tup]


class CourseForm(Form):
	course_title = SelectField('Course Title', choices=course_titles)
