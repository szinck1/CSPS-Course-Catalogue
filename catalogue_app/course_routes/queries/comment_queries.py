import pandas as pd
from catalogue_app.db import query_mysql


# Should probably store results_processed as attribute
class Comments:
	def __init__(self, course_code):
		self.course_code = course_code
		self.comment_data = None
		self.categorical_data = None
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
		# Query all comments and categorical questions
		self._load_all_comments()
		self._load_all_categorical()
		# Parse with Pandas and process into form required by Highcharts
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
		# Return False if course has received no feedback
		# Explicitely checking 'if df is False' rather than 'if not df' as
		# DataFrames do not have a truth value
		if self.comment_data is False:
			return False
		data_filtered = self.comment_data.loc[self.comment_data['short_question'] == question, :]
		results_processed = []
		for row in data_filtered.itertuples(index=False):
			# Unpack the tuple as some fields require customization
			text_answer = row[1]
			stars = int(row[2])
			learner_classif = row[3].replace(' - Unknown', '')
			offering_city = row[4].title().replace('(Ncr)', '(NCR)').replace("'S", "'s")
			fiscal_year = row[5].replace('-20', '-')
			quarter = row[6]
			# Reassemble and append
			tup = (text_answer, stars, learner_classif, offering_city, fiscal_year, quarter)
			results_processed.append(tup)
		return results_processed
	
	
	def _load_categorical(self, question):
		# Return False if course has received no feedback
		# Explicitely checking 'if df is False' rather than 'if not df' as
		# DataFrames do not have a truth value
		if self.categorical_data is False:
			return False
		data_filtered = self.categorical_data.loc[self.categorical_data['short_question'] == question, :]
		results_processed = []
		for row in data_filtered.itertuples(index=False):
			# Unpack the tuple as some fields require customization
			answer = row[1]
			count = row[2]
			# Reassemble and append
			dict_ = {'name': answer, 'y': count}
			results_processed.append(dict_)
		return results_processed if results_processed else [{'name': 'No response', 'y': 1}]
	
	
	def _load_all_comments(self):
		query = """
			SELECT short_question, text_answer, stars, learner_classif, offering_city, fiscal_year, quarter
			FROM comments
			WHERE
				course_code = %s
				AND
				short_question IN ('Comment - General', 'Comment - Technical', 'Comment - OL', 'Comment - Performance')
			ORDER BY RAND();
		"""
		results = query_mysql(query, (self.course_code,))
		results = pd.DataFrame(results, columns=['short_question', 'text_answer', 'stars', 'learner_classif',
												 'offering_city', 'fiscal_year', 'quarter'])
		# Account for learners who didn't submit stars with their comments
		results['stars'].fillna(0, inplace=True)
		# Return False if course has received no feedback
		self.comment_data = False if results.empty else results
	
	
	def _load_all_categorical(self):
		query = """
			SELECT short_question, text_answer, COUNT(text_answer)
			FROM comments
			WHERE
				course_code = %s
				AND
				short_question IN ('Reason to Participate', 'Technical Issues', 'OL Available', 'GCcampus Tools Used', 'Prep')
			GROUP BY short_question, text_answer
			ORDER BY 1 ASC;
		"""
		results = query_mysql(query, (self.course_code,))
		results = pd.DataFrame(results, columns=['short_question', 'text_answer', 'count'])
		# Return False if course has received no feedback
		self.categorical_data = False if results.empty else results
