from catalogue_app.db import query_mysql


def offering_city_counts(fiscal_year, course_code):
	table_name = 'lsr{0}'.format(fiscal_year)
	# Sort by count so that when overlapping markers are combined by function
	# _combine_overlapping_cities[_hashed], it's the city with the largest count into
	# which all others all merged
	query = """
		SELECT offering_city, COUNT(DISTINCT offering_id), offering_lat, offering_lng
		FROM {0}
		WHERE course_code = %s AND offering_status IN ('Open - Normal', 'Delivered - Normal')
		GROUP BY offering_city
		ORDER BY 2 DESC;
	""".format(table_name)
	results = query_mysql(query, (course_code,))
	# Make 'results' a list of lists so can be manipulated by JavaScript
	results = [[element for element in tup] for tup in results if tup[2] is not None]
	results = _combine_overlapping_cities_hashed(results)
	return results


def learner_city_counts(fiscal_year, course_code):
	table_name = 'lsr{0}'.format(fiscal_year)
	# Sort by count so that when overlapping markers are combined by function
	# _combine_overlapping_cities[_hashed], it's the city with the largest count into
	# which all others all merged
	query = """
		SELECT learner_city, COUNT(DISTINCT learner_id), learner_lat, learner_lng
		FROM {0}
		WHERE course_code = %s AND reg_status = 'Confirmed'
		GROUP BY learner_city
		ORDER BY 2 DESC;
	""".format(table_name)
	results = query_mysql(query, (course_code,))
	# Make 'results' a list of lists so can be manipulated by JavaScript
	results = [[element for element in tup] for tup in results if tup[2] is not None]
	results = _combine_overlapping_cities_hashed(results)
	return results


def _combine_overlapping_cities_hashed(my_list):
	"""If two cities' markers overlap, combine them into a single entry."""
	# Explanation: Use latitude and longitude rounded to N_DIGIT to create
	# a PKEY for each city. Log cities within dictionary and merge
	# overlapping cities. As queries above make use of 'ORDER BY x DESC',
	# the largest cities appear and are logged first. This means that e.g.
	# 2 occurrences of Kanata will be merged into Ottawa's 30 occurrences.
	N_DIGITS = 3
	merge_dict = {}
	# my_list is a list of lists
	# Each nested list has form ['city_name', count, latitude, longitude]
	for elem in my_list:
		city_name = elem[0]
		count = elem[1]
		# Python's 'round' internal func uses method 'round half to even'
		# https://en.wikipedia.org/wiki/Rounding#Round_half_to_even
		lat = round(elem[2], N_DIGITS)
		lng = round(elem[3], N_DIGITS)
		pkey = str(lat) + str(lng)
		# Log first occurrence
		if pkey not in merge_dict:
			# Log non-rounded values for maximum accuracy
			merge_dict[pkey] = [city_name, count, elem[2], elem[3]]
		# If lat/lng already logged, combine cities
		else:
			# print(f'Merging {city_name} into {merge_dict[pkey][0]}')
			merge_dict[pkey][1] += count
	# Return merge_dict's values in list
	mars = [value for value in merge_dict.values()]
	return mars


def _combine_overlapping_cities(my_list):
	"""If two cities' markers overlap, combine them into a single entry."""
	COMPARISON_DISTANCE = 0.005
	# my_list is a list of lists
	# Each nested list has form ['city_name', count, latitude, longitude]
	# Nested for loops to compare each element with all elements ahead of it
	for i in range(len(my_list) - 1):
		current_element = my_list[i]
		if current_element is None:
			continue
		for j in range(i + 1, len(my_list)):
			comparison_element = my_list[j]
			if comparison_element is None:
				continue
			# Check if cities overlap
			if (abs(current_element[2] - comparison_element[2]) < COMPARISON_DISTANCE) and \
				(abs(current_element[3] - comparison_element[3]) < COMPARISON_DISTANCE):
				# Take count away from comparison_element and set it to None
				# print(f'Merging {my_list[j][0]} into {my_list[i][0]}')
				my_list[i][1] += my_list[j][1]
				my_list[j] = None
	# Remove null entries	
	my_list = [elem for elem in my_list if elem is not None]
	return my_list
