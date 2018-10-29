from dashboards_app.config import Debug
from dashboards_app.dashboard_routes.utils import query_mysql
from wtforms import Form, SelectField

query = "SELECT DISTINCT course_title FROM lsr{0} ORDER BY 1 ASC;".format(Debug.THIS_YEAR)
results = query_mysql(query)
# SelectField takes a list of tuples
course_titles = [(val, val) for tup in results for val in tup]


class CourseForm(Form):
	course_title = SelectField('Course Title', choices=course_titles)
