from catalogue_app.db import query_mysql


class Comments:
	def __init__(self, course_code):
		self.course_code = course_code
		# Comments
		self.general = None
		self.technical = None
		self.language = None
		self.performance = None
		# Categorical and true/false questions
		self.reason = None
		self.technical_bool = None
		self.language_bool = None
		self.gccampus_bool = None
		self.preparation = None
	
	
	def load(self):
		# Comments
		self.general = self._load_comment('Comment - General')
		self.technical = self._load_comment('Comment - Technical')
		self.language = self._load_comment('Comment - OL')
		self.performance = self._load_comment('Comment - Performance')
		# Categorical and true/false questions
		self.reason = self._load_categorical('Reason to Participate')
		self.technical_bool = self._load_categorical('Technical Issues')
		self.language_bool = self._load_categorical('OL Available')
		self.gccampus_bool = self._load_categorical('GCcampus Tools Used')
		self.preparation = self._load_categorical('Prep')
		# Return self to allow method chaining
		return self
	
	
	def _load_comment(self, question):
		query = """
			SELECT text_answer, stars, learner_classif, offering_city, fiscal_year, quarter
			FROM comments
			WHERE course_code = %s AND short_question = %s
			ORDER BY RAND();
		"""
		results = query_mysql(query, (self.course_code, question))
		# Correct city names e.g. NORTH YORK -> North York via str.title()
		results = [(tup[0], tup[1], tup[2].replace(' - Unknown', ''), tup[3].title().replace('(Ncr)', '(NCR)').replace("'S", "'s"), tup[4].replace('-20', '-'), tup[5]) for tup in results]
		return results
	
	
	def _load_categorical(self, question):
		query = """
			SELECT text_answer, COUNT(text_answer)
			FROM comments
			WHERE course_code = %s AND short_question = %s
			GROUP BY text_answer
			ORDER BY 1 ASC;
		"""
		results = query_mysql(query, (self.course_code, question))
		# Process results into format required by Highcharts
		results_processed = []
		for tup in results:
			results_processed.append({'name': tup[0], 'y': tup[1]})
		return results_processed if results_processed else [{'name': 'No response', 'y': 1}]




















def fetch_comments(course_code, question):
	query = """
		SELECT text_answer, stars, learner_classif, offering_city, fiscal_year, quarter
		FROM comments
		WHERE course_code = %s AND short_question = %s
		ORDER BY RAND();
	"""
	results = query_mysql(query, (course_code, question))
	# Correct city names e.g. NORTH YORK -> North York via str.title()
	results = [(tup[0], tup[1], tup[2].replace(' - Unknown', ''), tup[3].title().replace('(Ncr)', '(NCR)').replace("'S", "'s"), tup[4].replace('-20', '-'), tup[5]) for tup in results]
	return results


def fetch_categorical(course_code, question):
	query = """
		SELECT text_answer, COUNT(text_answer)
		FROM comments
		WHERE course_code = %s AND short_question = %s
		GROUP BY text_answer
		ORDER BY 1 ASC;
	"""
	results = query_mysql(query, (course_code, question))
	
	# Process results into format required by Highcharts
	results_processed = []
	for tup in results:
		results_processed.append({'name': tup[0], 'y': tup[1]})
	return results_processed if results_processed else [{'name': 'No response', 'y': 1}]
