import csv
from io import StringIO
from catalogue_app.db import query_mysql

def general_tab(course_code):
	"""Query raw data used for the General tab."""
	query = """
		SELECT *
		FROM product_info
		WHERE course_code IN ('A313', 'A341')
	"""
	# Run query
	results = query_mysql(query, dict_=True)
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
	for dict_ in my_list[1:]:
		# Passing each key to dict is slow as requires each key
		# to be hashed. However, this method is safer than using
		# dict.values as lists produced guaranteed to follow correct
		# order. Note dicts in Python >= 3.6 preserve order.
		new_list = [dict_[column] for column in column_names]
		results_processed.append(new_list)
	return results_processed
