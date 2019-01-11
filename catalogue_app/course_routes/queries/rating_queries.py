from flask_babel import gettext
from catalogue_app.course_routes.utils import query_mysql


def all_ratings(course_code, lang):
	# Get list of questions answered for given course code
	field_name_1 = 'short_question_{0}'.format(lang)
	field_name_2 = 'long_question_{0}'.format(lang)
	questions_query = """
		SELECT DISTINCT {0}, {1}
		FROM ratings
		WHERE course_code = %s
		ORDER BY 1 ASC;
	""".format(field_name_1, field_name_2)
	questions = query_mysql(questions_query, (course_code,))
	# Account courses with no feedback
	if not questions:
		return False
	
	# Query each question for monthly results
	query = """
		SELECT month, numerical_answer, count
		FROM ratings
		WHERE course_code = %s AND {0} = %s;
	""".format(field_name_1)
	# Return a list of dictionaries
	return_list = []
	for question in questions:
		results = query_mysql(query, (course_code, question[0]))
		# Convert 'results' from format [(April, numerical_answer, count), ...] to {April: (numerical_answer, count), May: ...}
		results = [(tup[0], {'y': tup[1], 'count': tup[2]}) for tup in results]
		results = dict(results)
		results_processed = _add_months(results)
		return_list.append((question[0], question[1], results_processed))
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
