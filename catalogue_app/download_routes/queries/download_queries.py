import csv
from io import StringIO
from catalogue_app.config import Config
from catalogue_app.db import query_mysql

def general_tab(course_code):
	"""Query raw data used for the General tab."""
	query = """
		SELECT *
		FROM product_info
		WHERE course_code = %s;
	"""
	# Run query
	results = query_mysql(query, (course_code,), dict_=True)
	results_processed = _dicts_to_lists(results)
	# Write to CSV
	file = StringIO()
	csv_writer = csv.writer(file)
	csv_writer.writerows(results_processed)
	return file.getvalue()


def dashboard_tab(course_code):
	"""Query raw data used for the Dashboard tab."""
	THIS_YEAR = Config.THIS_YEAR
	table_name = 'lsr{0}'.format(THIS_YEAR)
	# Exclude course_title_en and course_title_fr
	# Saves a LOT of time, space for huge courses
	query = """
		SELECT course_code, business_type, offering_id, month_en,
			   month_fr, client, offering_status, offering_language,
			   offering_region_en, offering_region_fr, offering_province_en,
			   offering_province_fr, offering_city, offering_lat,
			   offering_lng, learner_province, learner_city, learner_lat,
			   learner_lng, reg_id, reg_status, no_show, learner_id,
			   learner_language, learner_classif, billing_dept_name_en,
			   billing_dept_name_fr
		FROM {0}
		WHERE course_code = %s;
	""".format(table_name)
	# Run query
	results = query_mysql(query, (course_code,), dict_=True)
	results_processed = _dicts_to_lists(results)
	# Write to CSV
	file = StringIO()
	csv_writer = csv.writer(file)
	csv_writer.writerows(results_processed)
	return file.getvalue()


def _dicts_to_lists(my_list):
	"""Convert list of dictionaries to list of lists, with first
	nested list containing column names.
	"""
	column_names = list(my_list[0].keys())
	results_processed = []
	results_processed.append(column_names)
	for dict_ in my_list:
		# Passing each key to dict is slow as requires each key
		# to be hashed. However, this method is safer than using
		# dict.values as lists produced guaranteed to follow correct
		# order. Note dicts in Python >= 3.6 preserve order.
		new_list = [dict_[column] for column in column_names]
		results_processed.append(new_list)
	return results_processed
