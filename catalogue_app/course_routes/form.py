import re
from dashboards_app.config import Debug
from dashboards_app.dashboard_routes.utils import query_mysql
from wtforms import Form, SelectField


# Internal func to remove course codes from titles
regex = re.compile(pattern=r'[(\[]{1}[a-zA-Z]{1}\d{3}[)\]]{1}')
def _clean_title(course_title):
	return regex.sub('', course_title).strip()


# Build form for courses
def course_form(lang, form_title):
	field_1 = 'course_title_{0}'.format(lang)
	table_name = 'lsr{}'.format(Debug.THIS_YEAR)
	query = """
			SELECT DISTINCT course_code, {0}
			FROM {1}
			ORDER BY 1 ASC;
			""".format(field_1, table_name)
	results = query_mysql(query)
	
	# SelectField takes list of tuples (pass_value, display_value)
	choices = [(tup[0], '{0}: {1}'.format(tup[0], _clean_title(tup[1]))) for tup in results]
	
	class CourseForm(Form):
		course_selection = SelectField(form_title, choices=choices)
	
	return CourseForm
