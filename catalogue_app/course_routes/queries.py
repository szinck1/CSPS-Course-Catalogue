from flask_babel import gettext
from catalogue_app.course_routes.utils import query_mysql, decimal_to_float, decimal_to_percent, decimal_to_int

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
		return course_title[0][0]


def general_info(lang, fiscal_year, course_code):
	table_name = 'lsr{0}'.format(fiscal_year)
	
	query_duration = "SELECT training_hours FROM {0} WHERE course_code = %s LIMIT 1;".format(table_name)
	duration = query_mysql(query_duration, (course_code,))
	
	field_name = 'stream_{0}'.format(lang)
	query_stream = "SELECT {0} FROM {1} WHERE course_code = %s LIMIT 1;".format(field_name, table_name)
	stream = query_mysql(query_stream, (course_code,))
	
	field_name = 'topic_{0}'.format(lang)
	query_topic = "SELECT {0} FROM {1} WHERE course_code = %s LIMIT 1;".format(field_name, table_name)
	topic = query_mysql(query_topic, (course_code,))
	
	query_open = "SELECT COUNT(DISTINCT offering_id) FROM {0} WHERE course_code = %s AND offering_status = 'Open - Normal';".format(table_name)
	open = query_mysql(query_open, (course_code,))
	
	query_delivered = "SELECT COUNT(DISTINCT offering_id) FROM {0} WHERE course_code = %s AND offering_status = 'Delivered - Normal';".format(table_name)
	delivered = query_mysql(query_delivered, (course_code,))
	
	query_cancelled = "SELECT COUNT(DISTINCT offering_id) FROM {0} WHERE course_code = %s AND offering_status = 'Cancelled - Normal';".format(table_name)
	cancelled = query_mysql(query_cancelled, (course_code,))
	
	query_client_reqs = "SELECT COUNT(DISTINCT offering_id) FROM {0} WHERE course_code = %s AND client != '';".format(table_name)
	client_reqs = query_mysql(query_client_reqs, (course_code,))
	
	query_regs = "SELECT COUNT(reg_num) FROM {0} WHERE course_code = %s AND reg_status = 'Confirmed';".format(table_name)
	regs = query_mysql(query_regs, (course_code,))
	
	query_no_shows = "SELECT SUM(no_show) FROM {0} WHERE course_code = %s;".format(table_name)
	no_shows = query_mysql(query_no_shows, (course_code,))
	
	results = [(gettext('Duration (hours)'), duration[0][0]),
			   (gettext('Stream'), stream[0][0]),
			   (gettext('Main Topic'), topic[0][0]),
			   (gettext('Open Offerings'), decimal_to_int(open)),
			   (gettext('Delivered Offerings'), decimal_to_int(delivered)),
			   (gettext('Cancelled Offerings'), decimal_to_int(cancelled)),
			   (gettext('Client Requests'), decimal_to_int(client_reqs)),
			   (gettext('Registrations'), decimal_to_int(regs)),
			   (gettext('No-Shows'), decimal_to_int(no_shows))]
	return results


def offerings_per_region(fiscal_year, course_code):
	table_name = 'lsr{0}'.format(fiscal_year)
	query = """
			SELECT offering_region_en, COUNT(DISTINCT offering_id)
			FROM {0}
			WHERE course_code = %s AND offering_status IN ('Open - Normal', 'Delivered - Normal')
			GROUP BY offering_region_en;
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
			SELECT offering_language_en, COUNT(DISTINCT offering_id)
			FROM {0}
			WHERE course_code = %s AND offering_status IN ('Open - Normal', 'Delivered - Normal')
			GROUP BY offering_language_en;
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
	return decimal_to_percent(results)


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
				SELECT COUNT(reg_num) AS class_size
				FROM {0}
				WHERE course_code LIKE %s AND reg_status= 'Confirmed'
				GROUP BY offering_id
				ORDER BY 1 DESC
			) AS sub_table;
			""".format(table_name)
	results = query_mysql(query, (course_code,))
	return decimal_to_int(results)


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
	return decimal_to_float(results)
