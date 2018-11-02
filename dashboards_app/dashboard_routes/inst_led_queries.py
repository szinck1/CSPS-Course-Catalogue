import json
from flask_babel import gettext
from dashboards_app.dashboard_routes.utils import query_mysql, decimal_to_float, decimal_to_int


def course_title(lang, fiscal_year, course_code):
	query = "SELECT course_title_{0} FROM lsr{1} WHERE course_code = '{2}' LIMIT 1;".format(lang, fiscal_year, course_code)
	course_title = query_mysql(query)
	return course_title[0][0]


def general_info(lang, fiscal_year, course_code):
	query_duration = "SELECT training_hours FROM lsr{0} WHERE course_code = '{1}' LIMIT 1;".format(fiscal_year, course_code)
	duration = query_mysql(query_duration)
	
	query_stream = "SELECT stream_{0} FROM lsr{1} WHERE course_code = '{2}' LIMIT 1;".format(lang, fiscal_year, course_code)
	stream = query_mysql(query_stream)
	
	query_topic = "SELECT topic_{0} FROM lsr{1} WHERE course_code = '{2}' LIMIT 1;".format(lang, fiscal_year, course_code)
	topic = query_mysql(query_topic)
	
	query_open = "SELECT COUNT(DISTINCT offering_id) FROM lsr{0} WHERE course_code = '{1}' AND offering_status = 'Open - Normal';".format(fiscal_year, course_code)
	open = query_mysql(query_open)
	
	query_delivered = "SELECT COUNT(DISTINCT offering_id) FROM lsr{0} WHERE course_code = '{1}' AND offering_status = 'Delivered - Normal';".format(fiscal_year, course_code)
	delivered = query_mysql(query_delivered)
	
	query_cancelled = "SELECT COUNT(DISTINCT offering_id) FROM lsr{0} WHERE course_code = '{1}' AND offering_status = 'Cancelled - Normal';".format(fiscal_year, course_code)
	cancelled = query_mysql(query_cancelled)
	
	query_client_reqs = "SELECT COUNT(DISTINCT offering_id) FROM lsr{0} WHERE course_code = '{1}' AND client != '';".format(fiscal_year, course_code)
	client_reqs = query_mysql(query_client_reqs)
	
	query_regs = "SELECT COUNT(reg_num) FROM lsr{0} WHERE course_code = '{1}' AND reg_status = 'Confirmed';".format(fiscal_year, course_code)
	regs = query_mysql(query_regs)
	
	query_no_shows = "SELECT SUM(no_show) FROM lsr{0} WHERE course_code = '{1}';".format(fiscal_year, course_code)
	no_shows = query_mysql(query_no_shows)
	
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


def offerings_per_region(lang, fiscal_year, course_code):
	query = """
			SELECT offering_region_{0}, COUNT(DISTINCT offering_id)
			FROM lsr{1}
			WHERE course_code = '{2}' AND offering_status IN ('Open - Normal', 'Delivered - Normal')
			GROUP BY offering_region_{0};
			""".format(lang, fiscal_year, course_code)
	results = query_mysql(query)
	
	# Process results into format required by Highcharts
	results = dict(results)
	results_processed = []
	if lang == 'fr':
		regions = ['Atlantique', 'Ontario', 'RCN', 'Pacifique', 'Prairie', 'Québec', 'Hors du Canada']
	else:
		regions = ['Atlantic', 'Ontario', 'NCR', 'Pacific', 'Prairie', 'Quebec', 'Outside Canada']
	for region in regions:
		count = results.get(region, 0)
		results_processed.append({'name': region, 'data': [count]})
	return json.dumps(results_processed)


def offerings_per_lang(lang, fiscal_year, course_code):
	query = """
			SELECT offering_language_{0}, COUNT(DISTINCT offering_id)
			FROM lsr{1}
			WHERE course_code = '{2}' AND offering_status IN ('Open - Normal', 'Delivered - Normal')
			GROUP BY offering_language_{0};
			""".format(lang, fiscal_year, course_code)
	results = query_mysql(query)
	
	# Process results into format required by Highcharts
	results = dict(results)
	results_processed = []
	for key, val in results.items():
		results_processed.append({'name': key, 'data': [val]})
	# Account for 0 offerings
	if not results_processed:
		if lang == 'fr':
			results_processed = [{'name': 'Anglais', 'data': [0]}, {'name': 'Français', 'data': [0]}]
		else:
			results_processed = [{'name': 'English', 'data': [0]}, {'name': 'French', 'data': [0]}]
	return json.dumps(results_processed)


# GOOD TIL THIS POINT


def offerings_cancelled(fiscal_year, course_code):
	query = """
			SELECT SUM(a.Mars / b.Mars)
			FROM
				(SELECT COUNT(DISTINCT offering_id) AS Mars
				 FROM lsr{0}
				 WHERE course_code LIKE '{1}' AND offering_status = 'Cancelled - Normal') AS a,
				 
				(SELECT COUNT(DISTINCT offering_id) AS Mars
				 FROM lsr{0}
				 WHERE course_code LIKE '{1}') AS b;
			""".format(fiscal_year, course_code)
	results = query_mysql(query)
	return decimal_to_float(results)


def top_5_depts(lang, fiscal_year, course_code):
	query = """
			SELECT billing_dept_name_{0}, COUNT(billing_dept_name_{0})
			FROM lsr{1}
			WHERE course_code = '{2}' AND reg_status = 'Confirmed'
			GROUP BY billing_dept_name_{0}
			ORDER BY 2 DESC
			LIMIT 5;
			""".format(lang, fiscal_year, course_code)
	return query_mysql(query)


def top_5_classifs(fiscal_year, course_code):
	query = """
			SELECT learner_classif, COUNT(learner_classif)
			FROM lsr{0}
			WHERE course_code = '{1}' AND reg_status = 'Confirmed'
			GROUP BY learner_classif
			ORDER BY 2 DESC
			LIMIT 5;
			""".format(fiscal_year, course_code)
	return query_mysql(query)


def avg_class_size(fiscal_year, course_code):
	query = """
			SELECT AVG(class_size)
			FROM(
				SELECT COUNT(reg_num) AS class_size
				FROM lsr{0}
				WHERE course_code LIKE '{1}' AND reg_status= 'Confirmed'
				GROUP BY offering_id
				ORDER BY 1 DESC
			) AS sub_table;
			""".format(fiscal_year, course_code)
	results = query_mysql(query)
	return decimal_to_int(results)


def avg_no_shows(fiscal_year, course_code):
	query = """
			SELECT SUM(a.Mars / b.Mars)
			FROM
				(SELECT SUM(no_show) AS Mars
				 FROM lsr{0}
				 WHERE course_code LIKE '{1}') AS a,
				 
				(SELECT COUNT(DISTINCT offering_id) AS Mars
				 FROM lsr{0}
				 WHERE course_code LIKE '{1}' AND offering_status IN ('Open - Normal', 'Delivered - Normal')) AS b;
			""".format(fiscal_year, course_code)
	results = query_mysql(query)
	return decimal_to_float(results)
