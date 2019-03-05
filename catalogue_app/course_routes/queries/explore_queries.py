import pandas as pd
from flask_babel import gettext
from catalogue_app.db import query_mysql


class CourseList:
	"""Data for the Explore tab, purpose of which is to allow users to 
	search by Provider, Business Line, and DG.
	"""
	def __init__(self, lang, fiscal_year):
		self.lang = lang
		self.fiscal_year = fiscal_year
		self.data = None
		self.business_lines = None
		self.providers = None
	
	
	def load(self):
		"""Run query and process all raw data."""
		self._load_courses()
		self._load_business_lines()
		self._load_providers()
		# Return self to allow method chaining
		return self
	
	
	def _load_courses(self):
		"""Query the DB and store results in DataFrame."""
		query = """
			SELECT DISTINCT b.provider_{0}, b.business_line_{0}, a.course_code, a.course_title_{0}
			FROM lsr{1} AS a
			LEFT OUTER JOIN product_info AS b
			ON a.course_code = b.course_code
			ORDER BY 1, 2, 3 ASC;
		""".format(self.lang, self.fiscal_year)
		results = query_mysql(query)
		results = pd.DataFrame(results, columns=['provider', 'business_line', 'course_code', 'course_title'])
		self.data = results
	
	
	def _load_business_lines(self):
		"""Get list of unique business lines."""
		business_lines = self.data.loc[:, 'business_line']
		business_lines.replace(['', None, 'None'], gettext('<awaiting mapping>'), inplace=True)
		business_lines = business_lines.unique()
		self.business_lines = business_lines
	
	
	def _load_providers(self):
		"""Get list of unique providers."""
		providers = self.data.loc[:, 'provider']
		providers.replace(['', None, 'None'], gettext('<awaiting mapping>'), inplace=True)
		providers = providers.unique()
		self.providers = providers
	
	
	def _get_courses(self, business_line, provider):
		"""For a given business line and provider, output list of
		associated course codes and course titles.
		"""
		business_line_bool = self.data['business_line'] == business_line
		provider_bool = self.data['provider'] == provider
		courses = self.data.loc[business_line_bool & provider_bool, ['course_code', 'course_title']].values.tolist()
		return courses
	
	
	def _get_nested_dicts(self):
		"""Create a nested dictionary based on self.business_lines and self.providers."""
		results = {}
		for business_line in self.business_lines:
			business_line_courses = {}
			for provider in self.providers:
				courses = self._get_courses(business_line, provider)
				if courses:
					business_line_courses[provider] = courses
			if business_line_courses:
				results[business_line] = business_line_courses
		return results
