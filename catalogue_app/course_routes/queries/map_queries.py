from catalogue_app.db import query_mysql


def offering_city_counts(fiscal_year, course_code):
	table_name = 'lsr{0}'.format(fiscal_year)
	query = """
		SELECT offering_city, COUNT(DISTINCT offering_id), offering_lat, offering_lng
		FROM {0}
		WHERE course_code = %s AND offering_status IN ('Open - Normal', 'Delivered - Normal')
		GROUP BY offering_city;
	""".format(table_name)
	results = query_mysql(query, (course_code,))
	# Make 'results' a list of lists so can be manipulated by JavaScript
	results = [[element for element in tup] for tup in results if tup[2] is not None]
	return results


def learner_city_counts(fiscal_year, course_code):
	table_name = 'lsr{0}'.format(fiscal_year)
	query = """
		SELECT learner_city, COUNT(DISTINCT learner_id), learner_lat, learner_lng
		FROM {0}
		WHERE course_code = %s AND reg_status = 'Confirmed'
		GROUP BY learner_city;
	""".format(table_name)
	results = query_mysql(query, (course_code,))
	# Make 'results' a list of lists so can be manipulated by JavaScript
	results = [[element for element in tup] for tup in results if tup[2] is not None]
	return results
