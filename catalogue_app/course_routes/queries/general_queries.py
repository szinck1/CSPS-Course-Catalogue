from flask_babel import gettext
from catalogue_app.course_routes.utils import query_mysql, as_string


def course_description(lang, course_code):
	field_name = 'course_description'
	query_description = "SELECT {0} FROM product_info WHERE course_code = %s LIMIT 1;".format(field_name)
	description = query_mysql(query_description, (course_code,))
	return as_string(description, error_msg='Apologies, this course is currently catalogued without a description.')


# Helper function to fetch product info
def _query_product_info(field, lang, course_code):
	field_name = field
	query = "SELECT {0} FROM product_info WHERE course_code = %s LIMIT 1;".format(field_name)
	result = query_mysql(query, (course_code,))
	return as_string(result, error_msg='<awaiting mapping>')


def course_info(lang, course_code):
	fields = [
		(gettext('Provider'), 'provider'),
		(gettext('Business Type'), 'business_type'),
		(gettext('Business Line'), 'business_line'),
		(gettext('Stream'), 'stream'),
		(gettext('Main Topic'), 'main_topic'),
		(gettext('Functional Area'), 'functional_area'),
		(gettext('Duration'), 'duration'),
		(gettext('Displayed on GCcampus'), 'displayed_on_gccampus'),
		(gettext('Required Training (as determined by TBS)'), 'required_training'),
		(gettext('Life Cycle Status'), 'life_cycle_status'),
		(gettext('Learning Outcome'), 'learning_outcome'),
		(gettext('Communities'), 'communities'),
		(gettext('Organization Unit'), 'organization_unit'),
		(gettext('Director'), 'director'),
		(gettext('Project Lead'), 'project_lead'),
		(gettext('Program Manager'), 'program_manager'),
		(gettext('Point of Contact'), 'point_of_contact')
	]
	results = {}
	for field in fields:
		results[field[0]] = _query_product_info(field[1], lang, course_code)
	return results
