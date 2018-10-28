from wtforms import Form, SelectField
from highcharts.inst_led import query_mysql
from main_config import Debug

query = "SELECT DISTINCT course_title FROM lsr{0} ORDER BY 1 ASC;".format(Debug.THIS_YEAR)
results = query_mysql(query)
# SelectField takes a list of tuples
course_titles = [(val, val) for tup in results for val in tup]


class CourseForm(Form):
	course_title = SelectField('Course Title', choices=course_titles)
