from catalogue_app.db import query_mysql
from catalogue_app.course_routes.utils import as_string


# Combine this with WTForms
def all_course_codes(fiscal_year):
	"""Funcs should all have docstrings + this one should
	be combined with those for the selection form.
	"""
	table_name = 'lsr{}'.format(fiscal_year)
	query = """
			SELECT DISTINCT course_code
			FROM {0}
			ORDER BY 1 ASC;
			""".format(table_name)
	results = query_mysql(query)
	results = [tup[0] for tup in results]
	return results


# Get this info simply from WTForms?
def course_title(lang, fiscal_year, course_code):
	field_name = 'course_title_{0}'.format(lang)
	table_name = 'lsr{0}'.format(fiscal_year)
	query = "SELECT {0} FROM {1} WHERE course_code = %s LIMIT 1;".format(field_name, table_name)
	course_title = query_mysql(query, (course_code,))
	return as_string(course_title, error_msg=False)


def course_info(course_code):
	query = "SELECT * FROM product_info WHERE course_code = %s LIMIT 1;"
	results = query_mysql(query, (course_code,), dict_=True)
	# Format keys for displaying on page
	results_processed = {_clean_key(key): val for (key, val) in results[0].items()}
	return results_processed


def _clean_key(key):
	key = key.title()
	replace_dict = {'Of': 'of', 'On': 'on', 'Gccampus': 'GCcampus', '_': ' '}
	for old, new in replace_dict.items():
		key = key.replace(old, new)
	return key
