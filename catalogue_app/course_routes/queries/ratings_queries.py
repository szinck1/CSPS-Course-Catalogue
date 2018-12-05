from flask_babel import gettext
from catalogue_app.course_routes.utils import query_mysql


def all_ratings(fiscal_year, course_code):
	table_name = 'ratings{0}'.format(fiscal_year)
	# Get list of questions answered for given course code
	questions_query = """
		SELECT DISTINCT short_question
		FROM {0}
		WHERE course_code = %s
		ORDER BY 1 ASC;
	""".format(table_name)
	questions = query_mysql(questions_query, (course_code,))
	questions = [tup[0] for tup in questions]
	# Account courses with no feedback
	if not questions:
		return False
	
	# Query each question for monthly results
	query = """
		SELECT month, numerical_answer
		FROM {0}
		WHERE course_code = %s AND short_question = %s;
	""".format(table_name)
	# Return a list of dictionaries
	return_list = []
	for question in questions:
		results = query_mysql(query, (course_code, question))
		results = dict(results)
		results_processed = _add_months(results)
		# Use str.title() method to nicely format question
		return_list.append((question.title(), results_processed))
	return return_list


# Helper function to ensure every month accounted for
def _add_months(my_dict):
	months = ['April', 'May', 'June', 'July', 'August', 'September', 'October',
			  'November']
	return_list = []
	for month in months:
		count = my_dict.get(month, 0)
		return_list.append(count)
	return return_list
