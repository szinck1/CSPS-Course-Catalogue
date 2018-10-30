from dashboards_app.config import Debug
from dashboards_app.dashboard_routes.utils import query_mysql
from wtforms import Form, SelectField


# Build form for Instructor-Led courses
inst_led_query = """
				 SELECT DISTINCT course_title
				 FROM lsr{0}
				 ORDER BY 1 ASC;
				 """.format(Debug.THIS_YEAR)
inst_led_results = query_mysql(inst_led_query)

# SelectField takes a list of tuples
inst_led_titles = [(val, val) for tup in inst_led_results for val in tup]


class InstLedForm(Form):
	course_title = SelectField('Course Title', choices=inst_led_titles)
