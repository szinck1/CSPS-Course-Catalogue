from catalogue_app.db import query_mysql


def validate_course_code(lang, fiscal_year, course_code):
	"""Check if course code exists in LSR. Return its title
	else False.
	"""
	field_name = 'course_title_{0}'.format(lang)
	table_name = 'lsr{0}'.format(fiscal_year)
	query = "SELECT {0} FROM {1} WHERE course_code = %s LIMIT 1;".format(field_name, table_name)
	course_title = query_mysql(query, (course_code,))
	return as_string(course_title, error_msg=False)


def as_string(my_val, error_msg=False):
	"""Helper function for returning a single value	from
	MySQL. Convert from [(my_val,)] to string.
	"""
	if not my_val or not my_val[0][0]:
		return error_msg
	else:
		return str(my_val[0][0])


def as_float(my_val):
	"""Helper function for returning a single value	from
	MySQL. Convert from [(my_val,)] to float.
	"""
	return float(as_string(my_val))


def as_int(my_val):
	"""Helper function for returning a single value	from
	MySQL. Convert from [(my_val,)] to int.
	"""
	return int(as_float(my_val))


def as_percent(my_val):
	"""Helper function for returning a single value	from
	MySQL. Convert from [(my_val,)] to percentage.
	"""
	return round(as_float(my_val), 2) * 100
