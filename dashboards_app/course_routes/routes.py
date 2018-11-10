from flask import Blueprint, redirect, render_template, request, session, url_for
from flask_babel import gettext
from dashboards_app.config import Debug
from dashboards_app.dashboard_routes.forms import course_form
import dashboards_app.dashboard_routes.course_queries as course_queries

dashboards = Blueprint('dashboards', __name__)

# Make LAST_YEAR and THIS_YEAR available to all templates
LAST_YEAR = Debug.LAST_YEAR
THIS_YEAR = Debug.THIS_YEAR
@dashboards.context_processor
def context_processor():
	return {'LAST_YEAR': LAST_YEAR.replace('_', '-'), 'THIS_YEAR': THIS_YEAR.replace('_', '-')}


# Form to get query parameters from user
@dashboards.route('/course-selection', methods=['GET', 'POST'])
def course_selection():
	field_title = gettext('Course Title')
	lang = session.get('lang', 'en')
	form = course_form(lang, field_title)
	form = form(request.form)
	
	if request.method == 'POST' and form.validate():
		course_code = form.course_selection.data
		return redirect(url_for('dashboards.course_result', course_code=course_code))
	return render_template('form.html', form=form, title=gettext("Selection"), button_val=gettext("Go"))


# Run queries and pass to + render template
@dashboards.route('/course-result')
def course_result():
	# Get arguments from query string; if incomplete, return to home page
	if 'course_code' not in request.args:
		return redirect(url_for('dashboards.course_selection'))
	# Automatically escaped in Jinja2 (HTML templates) and MySQL queries
	course_code = request.args['course_code']
	lang = session.get('lang', 'en')
	
	# If course_code doesn't exist, redirect to endroute not_found
	course_title = course_queries.course_title(lang, THIS_YEAR, course_code)
	if not course_title:
		return render_template('not-found.html')
	
	# Run queries and save in dict to be passed to templates
	pass_dict = {
		'course_code': course_code,
        'course_title': course_title,
		'general_info_LY': course_queries.general_info(lang, LAST_YEAR, course_code),
		'general_info_TY': course_queries.general_info(lang, THIS_YEAR, course_code),
		'offerings_per_region': course_queries.offerings_per_region(THIS_YEAR, course_code),
		'offerings_per_lang_LY': course_queries.offerings_per_lang(LAST_YEAR, course_code),
		'offerings_per_lang_TY': course_queries.offerings_per_lang(THIS_YEAR, course_code),
		'offerings_cancelled_overall_LY': course_queries.offerings_cancelled(LAST_YEAR, '%'),
		'offerings_cancelled_overall_TY': course_queries.offerings_cancelled(THIS_YEAR, '%'),
		'offerings_cancelled_LY': course_queries.offerings_cancelled(LAST_YEAR, course_code),
		'offerings_cancelled_TY': course_queries.offerings_cancelled(THIS_YEAR, course_code),
		'top_5_depts': course_queries.top_5_depts(lang, THIS_YEAR, course_code),
		'top_5_classifs': course_queries.top_5_classifs(THIS_YEAR, course_code),
		'avg_class_size_overall_LY': course_queries.avg_class_size(LAST_YEAR, '%'),
		'avg_class_size_overall_TY': course_queries.avg_class_size(THIS_YEAR, '%'),
		'avg_class_size_LY': course_queries.avg_class_size(LAST_YEAR, course_code),
		'avg_class_size_TY': course_queries.avg_class_size(THIS_YEAR, course_code),
		'avg_no_shows_overall_LY': round(course_queries.avg_no_shows(LAST_YEAR, '%'), 1),
		'avg_no_shows_overall_TY': round(course_queries.avg_no_shows(THIS_YEAR, '%'), 1),
		'avg_no_shows_LY': round(course_queries.avg_no_shows(LAST_YEAR, course_code), 1),
		'avg_no_shows_TY': round(course_queries.avg_no_shows(THIS_YEAR, course_code), 1)
	}
	return render_template('/course-page/main.html', pass_dict=pass_dict)


# Charts not yet implemented
@dashboards.route('/departmental')
def departmental():
	return render_template('departmental.html')
