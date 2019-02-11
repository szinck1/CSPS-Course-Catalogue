from flask_babel import gettext
from catalogue_app.db import query_mysql


def regs_per_month(lang, fiscal_year, course_code):
	field_name = 'month_{0}'.format(lang)
	table_name = 'lsr{0}'.format(fiscal_year)
	query = """
		SELECT {0}, COUNT(reg_id)
		FROM {1}
		WHERE course_code = %s AND reg_status = 'Confirmed'
		GROUP BY {0};
	""".format(field_name, table_name)
	results = query_mysql(query, (course_code,))
	results = dict(results)
	# Process results into format required by Highcharts
	results_processed = []
	# Ensure every month is returned, even if count 0
	months = [
		gettext('April'),
		gettext('May'),
		gettext('June'),
		gettext('July'),
		gettext('August'),
		gettext('September'),
		gettext('October'),
		gettext('November'),
		gettext('December'),
		gettext('January'),
		gettext('February'),
		gettext('March')
	]
	for month in months:
		count = results.get(month, 0)
		results_processed.append({'name': month, 'y': count})
	return results_processed


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
