import json
import mysql.connector
from configparser import ConfigParser

# Get config vals for MySQL
parser = ConfigParser()
parser.read('config.cfg')


# Internal function to query data from MySQL
def _query_mysql(query, all=True):
	cnx = mysql.connector.connect(user=parser.get('db', 'user'),
								  password=parser.get('db', 'password'),
								  host=parser.get('db', 'host'),
								  database=parser.get('db', 'database'))
	cursor = cnx.cursor()
	cursor.execute(query)
	results = cursor.fetchall() if all else cursor.fetchone()
	cnx.close()
	return results


def decimal_to_int(my_val):
	return int(float(str(my_val[0][0])))


def general_info(fiscal_year, course_title):
	query_duration = "SELECT training_hours FROM lsr{0} WHERE course_title = '{1}' LIMIT 1;".format(fiscal_year, course_title)
	duration = _query_mysql(query_duration, all=True)
	
	query_stream = "SELECT stream FROM lsr{0} WHERE course_title = '{1}' LIMIT 1;".format(fiscal_year, course_title)
	stream = _query_mysql(query_stream, all=True)
	
	query_topic = "SELECT topic FROM lsr{0} WHERE course_title = '{1}' LIMIT 1;".format(fiscal_year, course_title)
	topic = _query_mysql(query_topic, all=True)
	
	query_open = "SELECT COUNT(DISTINCT offering_id) FROM lsr{0} WHERE course_title = '{1}' AND offering_status = 'Open - Normal'".format(fiscal_year, course_title)
	open = _query_mysql(query_open, all=True)
	
	query_delivered = "SELECT COUNT(DISTINCT offering_id) FROM lsr{0} WHERE course_title = '{1}' AND offering_status = 'Delivered - Normal'".format(fiscal_year, course_title)
	delivered = _query_mysql(query_delivered, all=True)
	
	query_cancelled = "SELECT COUNT(DISTINCT offering_id) FROM lsr{0} WHERE course_title = '{1}' AND offering_status = 'Cancelled - Normal'".format(fiscal_year, course_title)
	cancelled = _query_mysql(query_cancelled, all=True)
	
	query_regs = "SELECT COUNT(reg_num) FROM lsr{0} WHERE course_title = '{1}' AND reg_status = 'Confirmed'".format(fiscal_year, course_title)
	regs = _query_mysql(query_regs, all=True)
	
	query_no_shows = "SELECT SUM(no_show) FROM lsr{0} WHERE course_title = '{1}'".format(fiscal_year, course_title)
	no_shows = _query_mysql(query_no_shows, all=True)
	
	results = [('Duration', duration[0][0]),
			   ('Stream', stream[0][0]),
			   ('Topic', topic[0][0]),
			   ('Open Offerings', open[0][0]),
			   ('Delivered Offerings', delivered[0][0]),
			   ('Cancelled Offerings', cancelled[0][0]),
			   ('Registrations', regs[0][0]),
			   ('No-Shows', decimal_to_int(no_shows))]
	
	return results






def top_5_depts(course_title):
	query = """
			SELECT billing_dept_name, COUNT(billing_dept_name)
			FROM lsr2018
			WHERE course_title = '{0}' AND reg_status = 'Confirmed' AND no_show = 0
			GROUP BY billing_dept_name
			ORDER BY 2 DESC
			LIMIT 5;
			""".format(course_title)
	return _query_mysql(query, all=True)


def top_5_classifs(course_title):
	query = """
			SELECT learner_classif, COUNT(learner_classif)
			FROM lsr2018
			WHERE course_title = '{0}' AND reg_status = 'Confirmed' AND no_show = 0
			GROUP BY learner_classif
			ORDER BY 2 DESC
			LIMIT 5;
			""".format(course_title)
	return _query_mysql(query, all=True)


def offerings_per_region(course_title):
	query = """
			SELECT offering_region, COUNT(DISTINCT offering_id)
			FROM lsr2018
			WHERE course_title = '{0}' AND offering_status IN ('Open - Normal', 'Delivered - Normal')
			GROUP BY offering_region;
			""".format(course_title)
	results = _query_mysql(query, all=True)
	
	# Process results into format required by Highcharts
	results = dict(results)
	results_processed = []
	all_regions = ['Atlantic', 'Ontario', 'NCR', 'Pacific', 'Prairie', 'Québec']
	for region in all_regions:
		count = results.get(region, 0)
		results_processed.append({'name': region, 'data': [count]})
	return json.dumps(results_processed)


def offerings_per_lang(course_title):
	query = """
			SELECT offering_language, COUNT(DISTINCT offering_id)
			FROM lsr2018
			WHERE course_title = '{0}' AND offering_status IN ('Open - Normal', 'Delivered - Normal')
			GROUP BY offering_language;
			""".format(course_title)
	results = _query_mysql(query, all=True)
	
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
				 WHERE course_code = '{1}' AND offering_status = 'Cancelled - Normal') a,
				 
				(SELECT COUNT(DISTINCT offering_id) AS Mars
				 FROM lsr{0}
				 WHERE course_code = '{1}') b;
			""".format(fiscal_year, course_title)
	pass


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
	results = _query_mysql(query, all=True)
	return decimal_to_int(results)
