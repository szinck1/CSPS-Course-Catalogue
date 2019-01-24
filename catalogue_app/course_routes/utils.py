# Make a class?

def as_string(my_val, error_msg=False):
	"""Convert from MySQL to Python dtypes."""
	# Account for MySQL returning NULL
	if not my_val or not my_val[0][0]:
		return error_msg
	else:
		return str(my_val[0][0])


def as_float(my_val):
	return float(as_string(my_val))


def as_int(my_val):
	return int(as_float(my_val))


def as_percent(my_val):
	return round(as_float(my_val), 2) * 100
