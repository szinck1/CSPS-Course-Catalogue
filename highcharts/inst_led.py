import json
import mysql.connector
from configparser import ConfigParser

# Get config vals for MySQL
parser = ConfigParser()
parser.read('./mysql_info/mysql_config.cfg')


# Internal function to query data from MySQL
def query_mysql(query, all=True):
	cnx = mysql.connector.connect(user=parser.get('db', 'user'),
								  password=parser.get('db', 'password'),
								  host=parser.get('db', 'host'),
								  database=parser.get('db', 'database'))
	cursor = cnx.cursor()
	cursor.execute(query)
	results = cursor.fetchall() if all else cursor.fetchone()
	cnx.close()
	return results


# Convert SQL datatype Decimal to Python float
def decimal_to_float(my_val):
	return float(str(my_val[0][0]))


# Convert SQL datatype Decimal to Python int
def decimal_to_int(my_val):
	return int(decimal_to_float(my_val))


def general_info(fiscal_year, course_title):
	query_duration = "SELECT training_hours FROM lsr{0} WHERE course_title = '{1}' LIMIT 1;".format(fiscal_year, course_title)
	duration = query_mysql(query_duration, all=True)
	
	query_stream = "SELECT stream FROM lsr{0} WHERE course_title = '{1}' LIMIT 1;".format(fiscal_year, course_title)
	stream = query_mysql(query_stream, all=True)
	
	query_topic = "SELECT topic FROM lsr{0} WHERE course_title = '{1}' LIMIT 1;".format(fiscal_year, course_title)
	topic = query_mysql(query_topic, all=True)
	
	query_open = "SELECT COUNT(DISTINCT offering_id) FROM lsr{0} WHERE course_title = '{1}' AND offering_status = 'Open - Normal';".format(fiscal_year, course_title)
	open = query_mysql(query_open, all=True)
	
	query_delivered = "SELECT COUNT(DISTINCT offering_id) FROM lsr{0} WHERE course_title = '{1}' AND offering_status = 'Delivered - Normal';".format(fiscal_year, course_title)
	delivered = query_mysql(query_delivered, all=True)
	
	query_cancelled = "SELECT COUNT(DISTINCT offering_id) FROM lsr{0} WHERE course_title = '{1}' AND offering_status = 'Cancelled - Normal';".format(fiscal_year, course_title)
	cancelled = query_mysql(query_cancelled, all=True)
	
	query_client_reqs = "SELECT COUNT(DISTINCT offering_id) FROM lsr{0} WHERE course_title = '{1}' AND client != '';".format(fiscal_year, course_title)
	client_reqs = query_mysql(query_client_reqs, all=True)
	
	query_regs = "SELECT COUNT(reg_num) FROM lsr{0} WHERE course_title = '{1}' AND reg_status = 'Confirmed';".format(fiscal_year, course_title)
	regs = query_mysql(query_regs, all=True)
	
	query_no_shows = "SELECT SUM(no_show) FROM lsr{0} WHERE course_title = '{1}';".format(fiscal_year, course_title)
	no_shows = query_mysql(query_no_shows, all=True)
	
	results = [('Duration', duration[0][0]),
			   ('Stream', stream[0][0]),
			   ('Topic', topic[0][0]),
			   ('Open Offerings', decimal_to_int(open)),
			   ('Delivered Offerings', decimal_to_int(delivered)),
			   ('Cancelled Offerings', decimal_to_int(cancelled)),
			   ('Client Requests', decimal_to_int(client_reqs)),
			   ('Registrations', decimal_to_int(regs)),
			   ('No-Shows', decimal_to_int(no_shows))]
	return results


def offerings_per_region(fiscal_year, course_title):
	query = """
			SELECT offering_region, COUNT(DISTINCT offering_id)
			FROM lsr{0}
			WHERE course_title = '{1}' AND offering_status IN ('Open - Normal', 'Delivered - Normal')
			GROUP BY offering_region;
			""".format(fiscal_year, course_title)
	results = query_mysql(query, all=True)
	
	# Process results into format required by Highcharts
	results = dict(results)
	results_processed = []
	all_regions = ['Atlantic', 'Ontario', 'NCR', 'Pacific', 'Prairie', 'Québec']
	for region in all_regions:
		count = results.get(region, 0)
		results_processed.append({'name': region, 'data': [count]})
	return json.dumps(results_processed)


def offerings_per_lang(fiscal_year, course_title):
	query = """
			SELECT offering_language, COUNT(DISTINCT offering_id)
			FROM lsr{0}
			WHERE course_title = '{1}' AND offering_status IN ('Open - Normal', 'Delivered - Normal')
			GROUP BY offering_language;
			""".format(fiscal_year, course_title)
	results = query_mysql(query, all=True)
	
	# Process results into format required by Highcharts
	results = dict(results)
	results_processed = []
	for key, val in results.items():
		results_processed.append({'name': key.split('/')[0], 'data': [val]})
	# Account for 0 offerings
	if not results_processed:
		results_processed = [{'name': 'English', 'data': [0]}, {'name': 'French', 'data': [0]}]
	return json.dumps(results_processed)


def offerings_cancelled(fiscal_year, course_title):
	query = """
			SELECT SUM(a.Mars / b.Mars)
			FROM
				(SELECT COUNT(DISTINCT offering_id) AS Mars
				 FROM lsr{0}
				 WHERE course_title LIKE '{1}' AND offering_status = 'Cancelled - Normal') AS a,
				 
				(SELECT COUNT(DISTINCT offering_id) AS Mars
				 FROM lsr{0}
				 WHERE course_title LIKE '{1}') AS b;
			""".format(fiscal_year, course_title)
	results = query_mysql(query, all=True)
	return decimal_to_float(results)


def top_5_depts(fiscal_year, course_title):
	query = """
			SELECT billing_dept_name, COUNT(billing_dept_name)
			FROM lsr{0}
			WHERE course_title = '{1}' AND reg_status = 'Confirmed' AND no_show = 0
			GROUP BY billing_dept_name
			ORDER BY 2 DESC
			LIMIT 5;
			""".format(fiscal_year, course_title)
	return query_mysql(query, all=True)


def top_5_classifs(fiscal_year, course_title):
	query = """
			SELECT learner_classif, COUNT(learner_classif)
			FROM lsr{0}
			WHERE course_title = '{1}' AND reg_status = 'Confirmed' AND no_show = 0
			GROUP BY learner_classif
			ORDER BY 2 DESC
			LIMIT 5;
			""".format(fiscal_year, course_title)
	return query_mysql(query, all=True)


def average_class_size(fiscal_year, course_title):
	query = """
			SELECT AVG(class_size)
			FROM(
				SELECT COUNT(reg_num) AS class_size
				FROM lsr{0}
				WHERE course_title LIKE '{1}' AND reg_status= 'Confirmed'
				GROUP BY offering_id
				ORDER BY 1 DESC
			) AS sub_table;
			""".format(fiscal_year, course_title)
	results = query_mysql(query, all=True)
	return decimal_to_int(results)


def no_shows(fiscal_year, course_title):
	query = """
			SELECT SUM(a.Mars / b.Mars)
			FROM
				(SELECT SUM(no_show) AS Mars
				 FROM lsr{0}
				 WHERE course_title LIKE '{1}') AS a,
				 
				(SELECT COUNT(DISTINCT offering_id) AS Mars
				 FROM lsr{0}
				 WHERE course_title LIKE '{1}' AND offering_status IN ('Open - Normal', 'Delivered - Normal')) AS b;
			""".format(fiscal_year, course_title)
	results = query_mysql(query, all=True)
	return decimal_to_float(results)
