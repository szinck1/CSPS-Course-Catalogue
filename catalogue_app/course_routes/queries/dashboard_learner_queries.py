from catalogue_app.course_routes.utils import query_mysql


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
