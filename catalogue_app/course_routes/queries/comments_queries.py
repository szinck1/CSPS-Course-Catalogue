from flask_babel import gettext
from catalogue_app.course_routes.utils import query_mysql


def general_comments(course_code):
	query = """
		SELECT text_answer, stars, learner_classif, offering_city
		FROM comments
		WHERE course_code = %s AND short_question IN ('Comment - general', 'Comment - General ', 'Comments', 'Comments  ')
		ORDER BY RAND();
		"""
	results = query_mysql(query, (course_code,))
	# Correct learner classifications e.g. "Big Cheese - Unknown" -> "Big Cheese"
	# Correct city names e.g. NORTH YORK -> North York
	results = [(tup[0], tup[1], tup[2].replace(' - Unknown', ''), tup[3].title().replace('(Ncr)', '(NCR)').replace("'S", "'s")) for tup in results]
	return results


def instructor_comments(course_code):
	query = """
		SELECT text_answer, stars, learner_classif, offering_city
		FROM comments
		WHERE course_code = %s AND short_question IN ('Comment - Instructor', 'Comments on Teacher', 'Comments on Guest Speaker')
		ORDER BY RAND();
		"""
	results = query_mysql(query, (course_code,))
	# Correct learner classifications e.g. "Big Cheese - Unknown" -> "Big Cheese"
	# Correct city names e.g. NORTH YORK -> North York
	results = [(tup[0], tup[1], tup[2].replace(' - Unknown', ''), tup[3].title().replace('(Ncr)', '(NCR)')) for tup in results]
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
