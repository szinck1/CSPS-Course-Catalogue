from flask_babel import gettext
from catalogue_app.db import query_mysql
from catalogue_app.course_routes.utils import as_string


class Learners:
	"""Data for the Learners section of the Dashboard tab."""
	def __init__(self, lang, fiscal_year, course_code):
		self.lang = lang
		self.fiscal_year = fiscal_year
		self.course_code = course_code
		self.regs_per_month = None
		self.top_classifs = None
		self.top_depts = None
		self.course_title = None
	
	
	def load(self):
		"""Run all learner queries."""
		self._calc_regs_per_month()
		self._calc_top_classifs()
		self._calc_top_depts()
		self._get_course_tile()
		# Return self to allow method chaining
		return self
	
	
	def _calc_regs_per_month(self):
		"""Query number of regisrations per month; include months
		that have 0 registrations.
		"""
		field_name = 'month_{0}'.format(self.lang)
		table_name = 'lsr{0}'.format(self.fiscal_year)
		query = """
			SELECT {0}, COUNT(reg_id)
			FROM {1}
			WHERE course_code = %s AND reg_status = 'Confirmed'
			GROUP BY {0};
		""".format(field_name, table_name)
		results = query_mysql(query, (self.course_code,))
		results = dict(results)
		# Process results into format required by Highcharts
		results_processed = []
		# Ensure every month is returned, even if count 0
		months = [
			gettext('April'),
			gettext('May'),
			gettext('June'),
			gettext('July'),
			gettext('August'),
			gettext('September'),
			gettext('October'),
			gettext('November'),
			gettext('December'),
			gettext('January'),
			gettext('February'),
			gettext('March')
		]
		for month in months:
			count = results.get(month, 0)
			results_processed.append({'name': month, 'y': count})
		self.regs_per_month = results_processed
	
	
	def _calc_top_classifs(self):
		"""Query the top classifications by number of registrations."""
		table_name = 'lsr{0}'.format(self.fiscal_year)
		query = """
			SELECT learner_classif, COUNT(learner_classif)
			FROM {0}
			WHERE course_code = %s AND reg_status = 'Confirmed'
			GROUP BY learner_classif
			ORDER BY 2 DESC
			LIMIT 5;
		""".format(table_name)
		results = query_mysql(query, (self.course_code,))
		self.top_classifs = results
	
	
	def _calc_top_depts(self):
		"""Query the top departments by number of registrations."""
		field_name =  'billing_dept_name_{0}'.format(self.lang)
		table_name = 'lsr{0}'.format(self.fiscal_year)
		query = """
			SELECT {0}, COUNT({0})
			FROM {1}
			WHERE course_code = %s AND reg_status = 'Confirmed'
			GROUP BY {0}
			ORDER BY 2 DESC
			LIMIT 5;
		""".format(field_name, table_name)
		results = query_mysql(query, (self.course_code,))
		self.top_depts = results
	
	
	def _get_course_tile(self):
		"""Get course title. In this module as should come from
		the lsr_fiscal_year table rather than the product_info
		table in case the course has registrations but has yet
		to be catalogued by CM."""
		field_name =  'course_title_{0}'.format(self.lang)
		table_name = 'lsr{0}'.format(self.fiscal_year)
		query = """
			SELECT {0}
			FROM {1}
			WHERE course_code = %s
			LIMIT 1;
		""".format(field_name, table_name)
		results = query_mysql(query, (self.course_code,))
		results = as_string(results)
		self.course_title = results
