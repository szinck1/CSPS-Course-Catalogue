from catalogue_app.db import query_mysql
from catalogue_app.course_routes.utils import as_string


def all_course_codes(fiscal_year):
	table_name = 'lsr{}'.format(fiscal_year)
	query = """
		SELECT DISTINCT course_code
		FROM {0}
		ORDER BY 1 ASC;
	""".format(table_name)
	results = query_mysql(query)
	results = [tup[0] for tup in results]
	return results


def course_title(lang, fiscal_year, course_code):
	field_name = 'course_title_{0}'.format(lang)
	table_name = 'lsr{0}'.format(fiscal_year)
	query = "SELECT {0} FROM {1} WHERE course_code = %s LIMIT 1;".format(field_name, table_name)
	course_title = query_mysql(query, (course_code,))
	return as_string(course_title, error_msg=False)


def course_info(lang, course_code):
	if lang == 'fr':
		fields = ['course_description_fr', 'business_type_fr', 'provider_fr',
		'displayed_on_gccampus_fr', 'duration', 'main_topic_fr', 'business_line_fr',
		'required_training_fr', 'communities_fr', 'point_of_contact', 'director',
		'program_manager', 'project_lead']
	else:
		fields = ['course_description_en', 'business_type_en', 'provider_en',
		'displayed_on_gccampus_en', 'duration', 'main_topic_en', 'business_line_en',
		'required_training_en', 'communities_en', 'point_of_contact', 'director',
		'program_manager', 'project_lead']
	
	query = "SELECT {0} FROM product_info WHERE course_code = %s LIMIT 1;".format(str(fields).replace('[', '').replace(']', '').replace("'", ''))
	results = query_mysql(query, (course_code,), dict_=True)
	# Account for new courses that have registrations but have yet to be catalogued
	if not results:
		return {}
	# Format keys for displaying on page
	results_processed = {_clean_key(key): val for (key, val) in results[0].items()}
	return results_processed


def _clean_key(key):
	# First remove endings _en and _fr
	# Then remove other underscores + junk
	key = key.title()
	replace_dict = {'_En': '', '_Fr': '', '_': ' ', 'Of': 'of', 'On': 'on', 'Gccampus': 'GCcampus'}
	for old, new in replace_dict.items():
		key = key.replace(old, new)
	return key
