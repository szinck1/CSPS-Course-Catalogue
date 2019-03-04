from catalogue_app.db import query_mysql


def course_list():
	query = """
		SELECT DISTINCT course_code, course_title_en
		FROM lsr2018_19
		ORDER BY 1 ASC;
	"""
	courses = query_mysql(query)
	
	results_processed = []
	for course in courses:
		my_list = [course[0], course[1], 'CSPS', 'Engineering Fundamentals']
		results_processed.append(my_list)
	return results_processed
