from flask_babel import gettext
from catalogue_app.course_routes.utils import query_mysql


def drf_average(fiscal_year, short_question, course_code):
	table_name = 'ratings{0}'.format(fiscal_year)
	query = """
	SELECT month, AVG(numerical_answer)
	FROM {0}
	WHERE course_code = %s AND short_question = %s
	GROUP BY month
	ORDER BY month_num;
	""".format(table_name)
	results = query_mysql(query, (course_code, short_question))
	
	# Process results into format required by Highcharts
	months = ['April', 'May', 'June', 'July', 'August', 'September', 'October',
			  'November', 'December', 'January', 'February', 'March']
	results = dict(results)
	results_processed = []
	for month in months:
		count = results.get(month, 0)
		count = round(float(count), 2)
		results_processed.append(count)
	return results_processed
