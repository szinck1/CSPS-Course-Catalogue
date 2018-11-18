from flask import Blueprint, redirect, render_template, request, session, url_for
from flask_babel import gettext
from catalogue_app.config import Debug
from catalogue_app.course_routes.form import course_form
import catalogue_app.course_routes.queries as queries

course = Blueprint('course', __name__)

# Make LAST_YEAR and THIS_YEAR available to all templates
LAST_YEAR = Debug.LAST_YEAR
THIS_YEAR = Debug.THIS_YEAR
@course.context_processor
def context_processor():
	return {'LAST_YEAR': LAST_YEAR.replace('_', '-'), 'THIS_YEAR': THIS_YEAR.replace('_', '-')}


# Form to get query parameters from user
@course.route('/course-selection', methods=['GET', 'POST'])
def course_selection():
	field_title = gettext('Course Title')
	lang = session.get('lang', 'en')
	form = course_form(lang, field_title)
	form = form(request.form)
	
	if request.method == 'POST' and form.validate():
		course_code = form.course_selection.data
		return redirect(url_for('course.course_result', course_code=course_code))
	return render_template('form.html', form=form, title=gettext("Selection"), button_val=gettext("Go"))


# Run queries and render template
@course.route('/course-result')
def course_result():
	# Get arguments from query string; if incomplete, return to selection page
	if 'course_code' not in request.args:
		return redirect(url_for('course.course_selection'))
	# Automatically escaped in Jinja2 (HTML templates) and MySQL queries
	course_code = request.args['course_code']
	lang = session.get('lang', 'en')
	
	# If course_code doesn't exist, render not_found.html
	course_title = queries.course_title(lang, THIS_YEAR, course_code)
	if not course_title:
		return render_template('not-found.html')
	
	# Run queries and save in dict to be passed to templates
	pass_dict = {
		#Global
		'course_code': course_code,
        'course_title': course_title,
		
		# Course Description
		'course_description': queries.course_description(lang, course_code),
		
		# Course Info
		'course_info': queries.course_info(lang, course_code),
		
		# Dashboard
		'overall_numbers_LY': queries.overall_numbers(LAST_YEAR, course_code),
		'overall_numbers_TY': queries.overall_numbers(THIS_YEAR, course_code),
		'offerings_per_region': queries.offerings_per_region(THIS_YEAR, course_code),
		'offerings_per_lang_LY': queries.offerings_per_lang(LAST_YEAR, course_code),
		'offerings_per_lang_TY': queries.offerings_per_lang(THIS_YEAR, course_code),
		'offerings_cancelled_global_LY': queries.offerings_cancelled_global(LAST_YEAR),
		'offerings_cancelled_global_TY': queries.offerings_cancelled_global(THIS_YEAR),
		'offerings_cancelled_LY': queries.offerings_cancelled(LAST_YEAR, course_code),
		'offerings_cancelled_TY': queries.offerings_cancelled(THIS_YEAR, course_code),
		'top_5_depts': queries.top_5_depts(lang, THIS_YEAR, course_code),
		'top_5_classifs': queries.top_5_classifs(THIS_YEAR, course_code),
		'avg_class_size_global_LY': queries.avg_class_size_global(LAST_YEAR),
		'avg_class_size_global_TY': queries.avg_class_size_global(THIS_YEAR),
		'avg_class_size_LY': queries.avg_class_size(LAST_YEAR, course_code),
		'avg_class_size_TY': queries.avg_class_size(THIS_YEAR, course_code),
		'avg_no_shows_global_LY': round(queries.avg_no_shows_global(LAST_YEAR), 1),
		'avg_no_shows_global_TY': round(queries.avg_no_shows_global(THIS_YEAR), 1),
		'avg_no_shows_LY': round(queries.avg_no_shows(LAST_YEAR, course_code), 1),
		'avg_no_shows_TY': round(queries.avg_no_shows(THIS_YEAR, course_code), 1),
		'general_comments': queries.general_comments(course_code)
	}
	return render_template('/course-page/main.html', pass_dict=pass_dict)


# Charts not yet implemented
@course.route('/departmental')
def departmental():
	return render_template('departmental.html')
