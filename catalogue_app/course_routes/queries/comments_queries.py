from flask_babel import gettext
from catalogue_app.course_routes.utils import query_mysql


def fetch_comments(question, course_code):
	query = """
		SELECT text_answer, stars, learner_classif, offering_city
		FROM comments
		WHERE course_code = %s AND short_question = '{0}'
		ORDER BY RAND();
		""".format(question)
	results = query_mysql(query, (course_code,))
	# Correct city names e.g. NORTH YORK -> North York via str.title()
	results = [(tup[0], tup[1], tup[2].replace(' - Unknown', ''), tup[3].title().replace('(Ncr)', '(NCR)').replace("'S", "'s")) for tup in results]
	return results


def reason_to_participate(course_code):
	query = """
	SELECT text_answer, COUNT(text_answer)
	FROM comments
	WHERE course_code = %s AND short_question = 'Reason to Participate'
	GROUP BY text_answer
	ORDER BY 1 ASC;
	"""
	results = query_mysql(query, (course_code,))
	
	# Process results into format required by Highcharts
	results_processed = []
	for tup in results:
		results_processed.append({'name': tup[0], 'y': tup[1]})
	return results_processed if results_processed else [{'name': 'No response', 'y': 1}]


def technical_issues(course_code):
	query = """
	SELECT text_answer, COUNT(text_answer)
	FROM comments
	WHERE course_code = %s AND short_question IN ('Technical Issues', 'Technical Issues?')
	GROUP BY text_answer
	ORDER BY 1 ASC;
	"""
	results = query_mysql(query, (course_code,))
	
	# Process results into format required by Highcharts
	results_processed = []
	for tup in results:
		results_processed.append({'name': tup[0], 'y': tup[1]})
	return results_processed if results_processed else [{'name': 'No response', 'y': 1}]
