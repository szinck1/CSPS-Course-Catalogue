from flask_babel import gettext
from catalogue_app.course_routes.utils import query_mysql


def all_ratings(course_code, lang):
	# Get list of questions answered for given course code
	field_name = 'short_question_{0}'.format(lang)
	questions_query = """
		SELECT DISTINCT {0}
		FROM ratings
		WHERE course_code = %s
		ORDER BY 1 ASC;
	""".format(field_name)
	questions = query_mysql(questions_query, (course_code,))
	questions = [tup[0] for tup in questions]
	# Account courses with no feedback
	if not questions:
		return False
	
	# Query each question for monthly results
	query = """
		SELECT month, numerical_answer, count
		FROM ratings
		WHERE course_code = %s AND {0} = %s;
	""".format(field_name)
	# Return a list of dictionaries
	return_list = []
	for question in questions:
		results = query_mysql(query, (course_code, question))
		# Convert 'results' from format [(month, numerical_answer, count), ...] to {month: (numerical_answer, count), ...}
		results = [(tup[0], {'y': tup[1], 'count': tup[2]}) for tup in results]
		results = dict(results)
		results_processed = _add_months(results)
		return_list.append((question, results_processed))
	return return_list


# Helper function to ensure every month accounted for
def _add_months(my_dict):
	months = ['April', 'May', 'June', 'July', 'August', 'September', 'October',
			  'November', 'December', 'January']
	return_list = []
	for month in months:
		count = my_dict.get(month, {'y': 0, 'count': 0})
		return_list.append(count)
	return return_list
