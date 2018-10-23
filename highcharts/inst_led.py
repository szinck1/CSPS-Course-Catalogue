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


def top_5_depts(course_title):
	query = """
			SELECT billing_dept_name, COUNT(billing_dept_name)
			FROM lsr
			WHERE course_title = '{0}' AND reg_status = 'Confirmed' AND no_show = 0
			GROUP BY billing_dept_name
			ORDER BY 2 DESC
			LIMIT 5;
			""".format(course_title)
	return _query_mysql(query, all=True)


def top_5_classifs(course_title):
	query = """
			SELECT learner_classif, COUNT(learner_classif)
			FROM lsr
			WHERE course_title = '{0}' AND reg_status = 'Confirmed' AND no_show = 0
			GROUP BY learner_classif
			ORDER BY 2 DESC
			LIMIT 5;
			""".format(course_title)
	return _query_mysql(query, all=True)


def offerings_per_region(course_title):
	query = """
			SELECT offering_region, COUNT(DISTINCT offering_id)
			FROM lsr
			WHERE course_title = '{0}' AND offering_status IN ('Open - Normal', 'Delivered - Normal')
			GROUP BY offering_region
			""".format(course_title)
	results = _query_mysql(query, all=True)
	
	# Process 'results' into format required by Highcharts
	results = dict(results)
	results_processed = []
	all_regions = ['Atlantic', 'Ontario', 'NCR', 'Pacific', 'Prairie', 'Québec']
	for region in all_regions:
		count = results.get(region, 0)
		results_processed.append({'name': region, 'data': [count]})
	return json.dumps(results_processed)


def offerings_per_lang(course_title):
	pass








