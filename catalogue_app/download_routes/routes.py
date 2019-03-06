import datetime
from flask import Blueprint, make_response, request
from flask_babel import gettext
from catalogue_app import auth
from catalogue_app.config import Config
from catalogue_app.course_routes import utils
from catalogue_app.download_routes.queries import download_queries

# Instantiate blueprint
downloads = Blueprint('downloads', __name__)


@downloads.route('/download-general')
@auth.login_required
def download_general():
	# Get course code from query string and validate
	course_code = request.args.get('course_code', False)
	# Point to query used for this tab
	query_func = download_queries.general_tab
	# Set filename
	filename = gettext('General Tab')
	# Run query and prepare file
	validate = _validate_course_code(course_code)
	raw_data = _run_query(validate, query_func, course_code)
	response = _create_response(raw_data, filename)
	return response


@downloads.route('/download-dashboard')
@auth.login_required
def download_dashboard():
	# Get course code from query string and validate
	course_code = request.args.get('course_code', False)
	# Point to query used for this tab
	query_func = download_queries.dashboard_tab
	# Set filename
	filename = gettext('Dashboard Tab')
	# Run query and prepare file
	validate = _validate_course_code(course_code)
	raw_data = _run_query(validate, query_func, course_code)
	response = _create_response(raw_data, filename)
	return response







def _validate_course_code(course_code):
	"""Ensure course code exists prior to proceeding."""
	# Inputs escaped in MySQL
	course_title = utils.validate_course_code('en', Config.THIS_YEAR, course_code)
	return True if course_title else False


def _run_query(validate, query_func, course_code):
	"""If course code successfully validated, query its raw
	data, else return error message.
	"""
	if validate:
		raw_data = query_func(course_code)
	else:
		raw_data = gettext('Course Not Found')
	return raw_data


def _create_response(raw_data, filename):
	"""Prepare file for download by browser."""
	output = make_response(raw_data)
	timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	# 'attachment' to ensure downloads rather than opened in browser
	output.headers['Content-Disposition'] = 'attachment; filename="{0} {1}.csv"'.format(filename, timestamp)
	output.headers['Content-Type'] = 'text/csv; charset=utf-8'
	return output
