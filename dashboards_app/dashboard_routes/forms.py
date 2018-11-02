import re
from dashboards_app.config import Debug
from dashboards_app.dashboard_routes.utils import query_mysql
from wtforms import Form, SelectField


# Internal func to remove course codes from titles
regex = re.compile(pattern=r'[(\[]{1}[a-zA-Z]{1}\d{3}[)\]]{1}')
def _clean_title(course_title):
	return regex.sub('', course_title).strip()


# Build form for Instructor-Led courses
def inst_led_form(lang, field_title):
	query = """
			SELECT DISTINCT course_code, course_title_{0}
			FROM lsr{1}
			ORDER BY 1 ASC;
			""".format(lang, Debug.LAST_YEAR)
	results = query_mysql(query)
	
	# SelectField takes list of tuples (pass_value, display_value)
	form_list = [(tup[0], '{0}: {1}'.format(tup[0], _clean_title(tup[1]))) for tup in results]
	
	class InstLedForm(Form):
		course_code = SelectField(field_title, choices=form_list)
	
	return InstLedForm
