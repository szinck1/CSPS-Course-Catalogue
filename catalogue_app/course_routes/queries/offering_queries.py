from collections import defaultdict
import pandas as pd
from flask_babel import gettext
from catalogue_app.db import query_mysql
from catalogue_app.course_routes.utils import as_string, as_float, as_int, as_percent

# Note: String interpolation used for 'lang' and 'fiscal_year' because:
# a) They exist only as server-side variables, aren't user inputs
# b) From MySQL docs at	http://mysql-python.sourceforge.net/MySQLdb.html
# "Parameter placeholders can only be used to insert column values."
# "They can not be used for other parts of SQL, such as table names, etc."


def overall_numbers(fiscal_year, course_code):
	"""Run queries for the 'Overall Numbers' section of the 'Dashboard' tab."""
	results = []
	component_1 = _offering_status_counts(fiscal_year, course_code)
	component_2 = _offering_additional_counts(fiscal_year, course_code)
	results.extend(component_1)
	results.extend(component_2)
	return results


def _offering_status_counts(fiscal_year, course_code):
	"""Query number of offerings by status for a given fiscal year."""
	table_name = 'lsr{0}'.format(fiscal_year)
	query = "SELECT offering_status, COUNT(DISTINCT offering_id) FROM {0} WHERE course_code = %s GROUP BY offering_status;".format(table_name)
	results = query_mysql(query, (course_code,))
	# Ensure all possible statuses returned (if count of 0, ignored by GROUP BY)
	results = dict(results)
	statuses = {
		gettext('Open Offerings'): 'Open - Normal',
		gettext('Delivered Offerings'): 'Delivered - Normal',
		gettext('Cancelled Offerings'): 'Cancelled - Normal'
	}
	results_processed = [(key, results.get(val, 0)) for (key, val) in statuses.items()]
	return results_processed


def _offering_additional_counts(fiscal_year, course_code):
	"""Additional information diplayed with _offering_status_counts."""
	table_name = 'lsr{0}'.format(fiscal_year)
	
	query_client_reqs = "SELECT COUNT(DISTINCT offering_id) FROM {0} WHERE course_code = %s AND client != '' AND offering_status IN ('Open - Normal', 'Delivered - Normal');".format(table_name)
	client_reqs = query_mysql(query_client_reqs, (course_code,))
	
	query_regs = "SELECT COUNT(reg_id) FROM {0} WHERE course_code = %s AND reg_status = 'Confirmed';".format(table_name)
	regs = query_mysql(query_regs, (course_code,))
	
	query_no_shows = "SELECT SUM(no_show) FROM {0} WHERE course_code = %s;".format(table_name)
	no_shows = query_mysql(query_no_shows, (course_code,))
	
	results = [(gettext('Client Requests'), as_int(client_reqs)),
			   (gettext('Registrations'), as_int(regs)),
			   (gettext('No-Shows'), as_int(no_shows))]
	return results


# This query probably needs an index
class OfferingLocations:
	def __init__(self, fiscal_year, course_code):
		self.fiscal_year = fiscal_year
		self.course_code = course_code
		self.data = None
	
	
	def load(self):
		table_name = 'lsr{0}'.format(self.fiscal_year)
		query = """
			SELECT offering_region, offering_province, offering_city, COUNT(DISTINCT offering_id)
			FROM {0}
			WHERE course_code = %s AND offering_status IN ('Open - Normal', 'Delivered - Normal')
			GROUP BY offering_region, offering_province, offering_city;
		""".format(table_name)
		results = query_mysql(query, (self.course_code,))
		results = pd.DataFrame(results, columns=['offering_region', 'offering_province', 'offering_city', 'count'])
		self.data = results
		# Return self to allow method chaining
		return self
	
	
	def region_drilldown(self):
		results = self.data.groupby('offering_region', as_index=False).sum()
		results_processed = dict(results.values.tolist())
		return results_processed
	
	
	def province_drilldown(self):
		# Get list of regions in which the course has offerings
		regions = self.data.loc[:, 'offering_region'].unique()
		# Counts by province
		counts = self.data.groupby(['offering_region', 'offering_province'], as_index=False).sum()
		# Process into form required by Highcharts
		results_processed = {}
		for region in regions:
			province_counts = counts.loc[counts['offering_region'] == region, ['offering_province', 'count']].values.tolist()
			province_counts_processed = self._process_counts(province_counts)
			results_processed[region] = province_counts_processed
		return results_processed
	
	
	def city_drilldown(self):
		# Get list of provinces in which the course has offerings
		provinces = self.data.loc[:, 'offering_province'].unique()
		# Counts by city
		counts = self.data.groupby(['offering_province', 'offering_city'], as_index=False).sum()
		# Process into form required by Highcharts
		results_processed = {}
		for province in provinces:
			city_counts = counts.loc[counts['offering_province'] == province, ['offering_city', 'count']].values.tolist()
			results_processed[province] = city_counts
		return results_processed
	
	
	@staticmethod
	def _process_counts(my_list):
		"""Take a nested list of form [['Ottawa', 10], ...] and covert to
		form [{'name': 'Ottawa', 'drilldown': 'Ottawa, 'y': 10}, ...]
		"""
		results_processed = [{'name': list_[0], 'drilldown': list_[0], 'y': list_[1]} for list_ in my_list]
		return results_processed


def offerings_per_lang(fiscal_year, course_code):
	table_name = 'lsr{0}'.format(fiscal_year)
	query = """
		SELECT offering_language, COUNT(DISTINCT offering_id)
		FROM {0}
		WHERE course_code = %s AND offering_status IN ('Open - Normal', 'Delivered - Normal')
		GROUP BY offering_language;
	""".format(table_name)
	results = query_mysql(query, (course_code,))
	
	# Force 'English', 'French', and 'Bilingual' to be returned within dict
	results = dict(results)
	if 'English' not in results:
		results['English'] = 0
	if 'French' not in results:
		results['French'] = 0
	if 'Bilingual' not in results:
		results['Bilingual'] = 0
	return results


def offerings_cancelled(fiscal_year, course_code):
	table_name = 'lsr{0}'.format(fiscal_year)
	query = """
		SELECT SUM(a.Mars / b.Mars)
		FROM
			(SELECT COUNT(DISTINCT offering_id) AS Mars
			 FROM {0}
			 WHERE course_code = %s AND offering_status = 'Cancelled - Normal') AS a,
			 
			(SELECT COUNT(DISTINCT offering_id) AS Mars
			 FROM {0}
			 WHERE course_code = %s) AS b;
	""".format(table_name)
	results = query_mysql(query, (course_code, course_code))
	return as_percent(results)


# Need to separate global into separate function as using LIKE '%' too slow
def offerings_cancelled_global(fiscal_year):
	table_name = 'lsr{0}'.format(fiscal_year)
	query = """
		SELECT SUM(a.Mars / b.Mars)
		FROM
			(SELECT COUNT(DISTINCT offering_id) AS Mars
			 FROM {0}
			 WHERE business_type = 'Instructor-Led' AND offering_status = 'Cancelled - Normal') AS a,
			 
			(SELECT COUNT(DISTINCT offering_id) AS Mars
			 FROM {0}
			 WHERE business_type = 'Instructor-Led') AS b;
	""".format(table_name)
	results = query_mysql(query)
	return as_percent(results)


def avg_class_size(fiscal_year, course_code):
	table_name = 'lsr{0}'.format(fiscal_year)
	query = """
		SELECT AVG(class_size)
		FROM(
			SELECT COUNT(reg_id) AS class_size
			FROM {0}
			WHERE course_code = %s AND reg_status= 'Confirmed'
			GROUP BY offering_id
		) AS sub_table;
	""".format(table_name)
	results = query_mysql(query, (course_code,))
	return as_int(results)


# Need to separate global into separate function as using LIKE '%' too slow
def avg_class_size_global(fiscal_year):
	table_name = 'lsr{0}'.format(fiscal_year)
	query = """
		SELECT AVG(class_size)
		FROM(
			SELECT COUNT(reg_id) AS class_size
			FROM {0}
			WHERE reg_status= 'Confirmed' AND business_type = 'Instructor-Led'
			GROUP BY offering_id
		) AS sub_table;
	""".format(table_name)
	results = query_mysql(query)
	return as_int(results)


def avg_no_shows(fiscal_year, course_code):
	table_name = 'lsr{0}'.format(fiscal_year)
	query = """
		SELECT SUM(a.Mars / b.Mars)
		FROM
			(SELECT SUM(no_show) AS Mars
			 FROM {0}
			 WHERE course_code = %s) AS a,
			 
			(SELECT COUNT(DISTINCT offering_id) AS Mars
			 FROM {0}
			 WHERE course_code = %s AND offering_status IN ('Open - Normal', 'Delivered - Normal')) AS b;
	""".format(table_name)
	results = query_mysql(query, (course_code, course_code))
	return as_float(results)


# Need to separate global into separate function as using LIKE '%' too slow
def avg_no_shows_global(fiscal_year):
	table_name = 'lsr{0}'.format(fiscal_year)
	query = """
		SELECT SUM(a.Mars / b.Mars)
		FROM
			(SELECT SUM(no_show) AS Mars
			 FROM {0}
			 WHERE no_show = 1) AS a,
			 
			(SELECT COUNT(DISTINCT offering_id) AS Mars
			 FROM {0}
			 WHERE business_type = 'Instructor-Led' AND offering_status IN ('Open - Normal', 'Delivered - Normal')) AS b;
	""".format(table_name)
	results = query_mysql(query)
	return as_float(results)
