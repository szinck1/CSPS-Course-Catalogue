import pandas as pd
from flask_babel import gettext
from catalogue_app.db import query_mysql


# This query probably needs an index
# Should probably store results_processed as attribute


class Ratings:
	def __init__(self, course_code, lang):
		self.course_code = course_code
		self.lang = lang
		self.data = None
	
	
	def load(self):
		field_name_1 = 'short_question_{0}'.format(self.lang)
		field_name_2 = 'long_question_{0}'.format(self.lang)
		query = """
			SELECT {0}, {1}, month, numerical_answer, count
			FROM ratings
			WHERE course_code = %s;
		""".format(field_name_1, field_name_2)
		results = query_mysql(query, (self.course_code,))
		results = pd.DataFrame(results, columns=['short_question', 'long_question', 'month', 'average', 'count'])
		# Return False if course has received no feedback
		self.data = False if results.empty else results
		# Return self to allow method chaining
		return self
	
	
	def all_ratings(self):
		# Get list of questions for which the course has answers
		questions = self.data.loc[:, ['short_question', 'long_question']].drop_duplicates(inplace=False)
		# Process into form required by Highcharts
		results_processed = []
		for question in questions.itertuples(index=False):
			short_question = question[0]
			long_question = question[1]
			question_data = self.data.loc[self.data['short_question'] == short_question, ['month', 'average', 'count']]
			monthly_values = self._get_monthly_values(question_data)
			results_processed.append((short_question, long_question, monthly_values))
		return results_processed
	
	
	@staticmethod
	def _get_monthly_values(df):
		months = ['February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
				  'October', 'November', 'December', 'January']
		monthly_values = []
		for month in months:
			df_month = df.loc[df['month'] == month, :]
			try:
				average = df_month.iloc[0]['average']
				count = df_month.iloc[0]['count']
			except IndexError:
				average = 0
				count = 0
			monthly_values.append({'y': average, 'count': count})
		return monthly_values
