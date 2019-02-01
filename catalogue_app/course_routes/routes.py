import copy
import pickle
import time
from flask import Blueprint, redirect, render_template, request, session, url_for
from flask_babel import gettext
from catalogue_app import auth
from catalogue_app.config import Config
from catalogue_app.course_routes.forms import course_form
from catalogue_app.course_routes.queries import (
	comment_queries, general_queries, learner_queries, map_queries, memoize_func, offering_queries, rating_queries
)

# Instantiate blueprint
course = Blueprint('course', __name__)


# Make LAST_YEAR and THIS_YEAR available to all templates
LAST_YEAR = Config.LAST_YEAR
THIS_YEAR = Config.THIS_YEAR
@course.context_processor
def context_processor():
	return {'LAST_YEAR': LAST_YEAR.replace('_', '-'), 'THIS_YEAR': THIS_YEAR.replace('_', '-')}


# Course selection
@course.route('/course-selection', methods=['GET', 'POST'])
@auth.login_required
def course_selection():
	# Only allow 'en' and 'fr' to be passed to app
	lang = 'fr' if request.cookies.get('lang', None) == 'fr' else 'en'
	form = course_form(lang)
	form = form(request.form)
	
	if request.method == 'POST' and form.validate():
		course_code = form.course_selection.data
		return redirect(url_for('course.course_result', course_code=course_code))
	return render_template('form.html', form=form, title=gettext("Selection"), button_val=gettext("Go"))


# Catalogue's entry for a given course: the meat & potatoes of the app
@course.route('/course-result')
@auth.login_required
def course_result():
	### VALIDATION ###
	# Get arguments from query string; if incomplete, return to selection page
	if 'course_code' not in request.args:
		return redirect(url_for('course.course_selection'))
	# Argument is automatically escaped in Jinja2 (HTML templates) and MySQL queries
	course_code = request.args['course_code']
	# Only allow 'en' and 'fr' to be passed to app
	lang = 'fr' if request.cookies.get('lang', None) == 'fr' else 'en'
	# Security check: If course_code doesn't exist, render not_found.html
	course_title = general_queries.course_title(lang, THIS_YEAR, course_code)
	if not course_title:
		return render_template('not-found.html')
	
	### QUERYING ###
	# Instantiate classes
	locations = offering_queries.OfferingLocations(lang, THIS_YEAR, course_code).load()
	ratings = rating_queries.Ratings(lang, course_code).load()
	comments = comment_queries.Comments(course_code).load()
	pass_dict = {
		#Global
		'course_code': course_code,
		'course_title': course_title,
		# General
		'course_info': general_queries.course_info(lang, course_code),
		# Dashboard - offerings
		'overall_numbers_LY': offering_queries.overall_numbers(LAST_YEAR, course_code),
		'overall_numbers_TY': offering_queries.overall_numbers(THIS_YEAR, course_code),
		'region_drilldown': locations.region_drilldown(),
		'province_drilldown': locations.province_drilldown(),
		'city_drilldown': locations.city_drilldown(),
		'offerings_per_lang_LY': offering_queries.offerings_per_lang(LAST_YEAR, course_code),
		'offerings_per_lang_TY': offering_queries.offerings_per_lang(THIS_YEAR, course_code),
		'offerings_cancelled_global_LY': offering_queries.offerings_cancelled_global(LAST_YEAR),
		'offerings_cancelled_global_TY': offering_queries.offerings_cancelled_global(THIS_YEAR),
		'offerings_cancelled_LY': offering_queries.offerings_cancelled(LAST_YEAR, course_code),
		'offerings_cancelled_TY': offering_queries.offerings_cancelled(THIS_YEAR, course_code),
		'avg_class_size_global_LY': offering_queries.avg_class_size_global(LAST_YEAR),
		'avg_class_size_global_TY': offering_queries.avg_class_size_global(THIS_YEAR),
		'avg_class_size_LY': offering_queries.avg_class_size(LAST_YEAR, course_code),
		'avg_class_size_TY': offering_queries.avg_class_size(THIS_YEAR, course_code),
		'avg_no_shows_global_LY': round(offering_queries.avg_no_shows_global(LAST_YEAR), 1),
		'avg_no_shows_global_TY': round(offering_queries.avg_no_shows_global(THIS_YEAR), 1),
		'avg_no_shows_LY': round(offering_queries.avg_no_shows(LAST_YEAR, course_code), 1),
		'avg_no_shows_TY': round(offering_queries.avg_no_shows(THIS_YEAR, course_code), 1),
		# Dashboard - learners
		'regs_per_month': learner_queries.regs_per_month(lang, THIS_YEAR, course_code),
		'top_5_depts': learner_queries.top_5_depts(lang, THIS_YEAR, course_code),
		'top_5_classifs': learner_queries.top_5_classifs(THIS_YEAR, course_code),
		# Maps
		'offering_city_counts': map_queries.offering_city_counts(THIS_YEAR, course_code),
		'learner_city_counts': map_queries.learner_city_counts(THIS_YEAR, course_code),
		# Ratings
		'all_ratings': ratings.all_ratings(),
		# Comments
		'general_comments': comments.general,
		'technical_comments': comments.technical,
		'language_comments': comments.language,
		'performance_comments': comments.performance,
		# Categorical and yes/no questions
		'reason_to_participate': comments.reason,
		'technical_issues': comments.technical_bool,
		'languages_available': comments.language_bool,
		'tools_used': comments.gccampus_bool,
		'prepared_by': comments.preparation
	}
	return render_template('/course-page/main.html', pass_dict=pass_dict)


# Temporary solution: Run queries for all course codes, store in dict, export to pickle
@course.route('/memoize-all')
@auth.login_required
def memoize_all():
	t1 = time.time()
	memo_dict = {}
	course_codes = general_queries.all_course_codes(THIS_YEAR)
	for code in course_codes:
		vals = memoize_func.get_vals(code)
		memo_dict[code] = vals
		print(code)
	t2 = time.time()
	# Save memo_dict to binary file
	with open('memo.pickle', 'wb') as f:
		pickle.dump(memo_dict, f, protocol=pickle.HIGHEST_PROTOCOL)
	return '<h1>Done!</h1><p>Time elapsed: {0}</p><p>Another great day in DIS.</p>'.format(t2 - t1)


# Coming soon
@course.route('/departmental')
@auth.login_required
def departmental():
	return render_template('departmental.html')
