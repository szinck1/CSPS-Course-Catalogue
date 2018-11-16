from flask_babel import gettext
from catalogue_app.course_routes.utils import query_mysql, as_string, as_float, as_int, as_percent

# Note: String interpolation used for 'lang' and 'fiscal_year' because:
# a) They exist only as server-side variables, aren't user inputs
# b) From MySQL docs at	http://mysql-python.sourceforge.net/MySQLdb.html
# "Parameter placeholders can only be used to insert column values."
# "They can not be used for other parts of SQL, such as table names, etc."


def course_title(lang, fiscal_year, course_code):
	field_name = 'course_title_{0}'.format(lang)
	table_name = 'lsr{0}'.format(fiscal_year)
	
	query = "SELECT {0} FROM {1} WHERE course_code = %s LIMIT 1;".format(field_name, table_name)
	course_title = query_mysql(query, (course_code,))
	if not course_title:
		return False
	else:
		return as_string(course_title)


def course_description(lang, course_code):
	# field_name = 'Course_Description_{0}'.format(lang)
	field_name = 'course_description'
	query_description = "SELECT {0} FROM product_info WHERE course_code = %s LIMIT 1;".format(field_name)
	description = query_mysql(query_description, (course_code,))
	return as_string(description)


# Helper function to fetch product info
def _query_product_info(field, lang, course_code):
	# field_name = '{0}_{1}'.format(field, lang)
	field_name = field
	query = "SELECT {0} FROM product_info WHERE course_code = %s LIMIT 1;".format(field_name)
	result = query_mysql(query, (course_code,))
	result = as_string(result)
	return result if result else gettext('Product not yet catalogued')


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
	results = []
	for field in fields:
		results.append((field[0], _query_product_info(field[1], lang, course_code)))
	return results


def overall_numbers(fiscal_year, course_code):
	table_name = 'lsr{0}'.format(fiscal_year)
	
	query_open = "SELECT COUNT(DISTINCT offering_id) FROM {0} WHERE course_code = %s AND offering_status = 'Open - Normal';".format(table_name)
	open = query_mysql(query_open, (course_code,))
	
	query_delivered = "SELECT COUNT(DISTINCT offering_id) FROM {0} WHERE course_code = %s AND offering_status = 'Delivered - Normal';".format(table_name)
	delivered = query_mysql(query_delivered, (course_code,))
	
	query_cancelled = "SELECT COUNT(DISTINCT offering_id) FROM {0} WHERE course_code = %s AND offering_status = 'Cancelled - Normal';".format(table_name)
	cancelled = query_mysql(query_cancelled, (course_code,))
	
	query_client_reqs = "SELECT COUNT(DISTINCT offering_id) FROM {0} WHERE course_code = %s AND client != '';".format(table_name)
	client_reqs = query_mysql(query_client_reqs, (course_code,))
	
	query_regs = "SELECT COUNT(reg_id) FROM {0} WHERE course_code = %s AND reg_status = 'Confirmed';".format(table_name)
	regs = query_mysql(query_regs, (course_code,))
	
	query_no_shows = "SELECT SUM(no_show) FROM {0} WHERE course_code = %s;".format(table_name)
	no_shows = query_mysql(query_no_shows, (course_code,))
	
	results = [(gettext('Open Offerings'), as_int(open)),
			   (gettext('Delivered Offerings'), as_int(delivered)),
			   (gettext('Cancelled Offerings'), as_int(cancelled)),
			   (gettext('Client Requests'), as_int(client_reqs)),
			   (gettext('Registrations'), as_int(regs)),
			   (gettext('No-Shows'), as_int(no_shows))]
	return results


def offerings_per_region(fiscal_year, course_code):
	table_name = 'lsr{0}'.format(fiscal_year)
	query = """
			SELECT offering_region, COUNT(DISTINCT offering_id)
			FROM {0}
			WHERE course_code = %s AND offering_status IN ('Open - Normal', 'Delivered - Normal')
			GROUP BY offering_region;
			""".format(table_name)
	results = query_mysql(query, (course_code,))
	results = dict(results)
	
	# Process results into format required by Highcharts
	results_processed = {}
	regions = ['Atlantic', 'NCR', 'Ontario', 'Pacific', 'Prairie', 'Quebec', 'Outside Canada']
	for region in regions:
		count = results.get(region, 0)
		results_processed[region] = count
	return results_processed


def offerings_per_lang(fiscal_year, course_code):
	table_name = 'lsr{0}'.format(fiscal_year)
	query = """
			SELECT offering_language, COUNT(DISTINCT offering_id)
			FROM {0}
			WHERE course_code = %s AND offering_status IN ('Open - Normal', 'Delivered - Normal')
			GROUP BY offering_language;
			""".format(table_name)
	results = query_mysql(query, (course_code,))
	
	# Force 'English', 'French', and 'Bilingual' to be returned within dict
	results = dict(results)
	if 'English' not in results:
		results['English'] = 0
	if 'French' not in results:
		results['French'] = 0
	if 'Bilingual' not in results:
		results['Bilingual'] = 0
	return results


def offerings_cancelled(fiscal_year, course_code):
	table_name = 'lsr{0}'.format(fiscal_year)
	query = """
			SELECT SUM(a.Mars / b.Mars)
			FROM
				(SELECT COUNT(DISTINCT offering_id) AS Mars
				 FROM {0}
				 WHERE course_code LIKE %s AND offering_status = 'Cancelled - Normal') AS a,
				 
				(SELECT COUNT(DISTINCT offering_id) AS Mars
				 FROM {0}
				 WHERE course_code LIKE %s) AS b;
			""".format(table_name)
	results = query_mysql(query, (course_code, course_code))
	return as_percent(results)


def top_5_depts(lang, fiscal_year, course_code):
	field_name =  'billing_dept_name_{0}'.format(lang)
	table_name = 'lsr{0}'.format(fiscal_year)
	
	query = """
			SELECT {0}, COUNT({0})
			FROM {1}
			WHERE course_code = %s AND reg_status = 'Confirmed'
			GROUP BY {0}
			ORDER BY 2 DESC
			LIMIT 5;
			""".format(field_name, table_name)
	return query_mysql(query, (course_code,))


def top_5_classifs(fiscal_year, course_code):
	table_name = 'lsr{0}'.format(fiscal_year)
	query = """
			SELECT learner_classif, COUNT(learner_classif)
			FROM {0}
			WHERE course_code = %s AND reg_status = 'Confirmed'
			GROUP BY learner_classif
			ORDER BY 2 DESC
			LIMIT 5;
			""".format(table_name)
	return query_mysql(query, (course_code,))


def avg_class_size(fiscal_year, course_code):
	table_name = 'lsr{0}'.format(fiscal_year)
	query = """
			SELECT AVG(class_size)
			FROM(
				SELECT COUNT(reg_id) AS class_size
				FROM {0}
				WHERE course_code LIKE %s AND reg_status= 'Confirmed'
				GROUP BY offering_id
				ORDER BY 1 DESC
			) AS sub_table;
			""".format(table_name)
	results = query_mysql(query, (course_code,))
	return as_int(results)


def avg_no_shows(fiscal_year, course_code):
	table_name = 'lsr{0}'.format(fiscal_year)
	query = """
			SELECT SUM(a.Mars / b.Mars)
			FROM
				(SELECT SUM(no_show) AS Mars
				 FROM {0}
				 WHERE course_code LIKE %s) AS a,
				 
				(SELECT COUNT(DISTINCT offering_id) AS Mars
				 FROM {0}
				 WHERE course_code LIKE %s AND offering_status IN ('Open - Normal', 'Delivered - Normal')) AS b;
			""".format(table_name)
	results = query_mysql(query, (course_code, course_code))
	return as_float(results)
