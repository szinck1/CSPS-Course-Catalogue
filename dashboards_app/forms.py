from dashboards_app import THIS_YEAR
from dashboards_app.inst_led import query_mysql
from wtforms import Form, SelectField

query = "SELECT DISTINCT course_title FROM lsr{0} ORDER BY 1 ASC;".format(THIS_YEAR)
results = query_mysql(query)
# SelectField takes a list of tuples
course_titles = [(val, val) for tup in results for val in tup]


class CourseForm(Form):
	course_title = SelectField('Course Title', choices=course_titles)
