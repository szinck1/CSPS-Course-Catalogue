from flask import Blueprint, redirect, render_template, request, session, url_for
from flask_babel import gettext
from dashboards_app.config import Debug
from dashboards_app.dashboard_routes.forms import inst_led_form
import dashboards_app.dashboard_routes.inst_led_queries as inst_led_queries

dashboards = Blueprint('dashboards', __name__)

# Make LAST_YEAR and THIS_YEAR available to all templates
LAST_YEAR = Debug.LAST_YEAR
THIS_YEAR = Debug.THIS_YEAR
@dashboards.context_processor
def context_processor():
	return {'LAST_YEAR': LAST_YEAR.replace('_', '-'), 'THIS_YEAR': THIS_YEAR.replace('_', '-')}


# Form to get query parameters from user
@dashboards.route('/instructor-led', methods=['GET', 'POST'])
def instructor_led():
	field_title = gettext('Course Title')
	lang = session.get('lang', 'en')
	form = inst_led_form(lang, field_title)
	form = form(request.form)
	
	if request.method == 'POST' and form.validate():
		course_code = form.course_code.data
		return redirect(url_for('dashboards.instructor_led_dash', course_code=course_code))
	return render_template('form.html', form=form, title=gettext("Dashboard Parameters"), button_val=gettext("Go"))


# Run queries and pass to + render template
@dashboards.route('/instructor-led-dash')
def instructor_led_dash():
	# Get arguments from query string; if incomplete, return to home page
	if 'course_code' not in request.args:
		return redirect(url_for('dashboards.instructor_led'))
	course_code = request.args['course_code']
	lang = session.get('lang', 'en')
	
	# Run queries and save in dict to be passed to templates
	pass_dict = {
		'course_code': course_code,
        'course_title': inst_led_queries.course_title(lang, THIS_YEAR, course_code),
		'general_info_LY': inst_led_queries.general_info(lang, LAST_YEAR, course_code),
		'general_info_TY': inst_led_queries.general_info(lang, THIS_YEAR, course_code),
		'offerings_per_region': inst_led_queries.offerings_per_region(lang, THIS_YEAR, course_code),
		'offerings_per_lang': inst_led_queries.offerings_per_lang(lang, THIS_YEAR, course_code),
		'offerings_cancelled_overall_LY': inst_led_queries.offerings_cancelled(LAST_YEAR, '%'),
		'offerings_cancelled_overall_TY': inst_led_queries.offerings_cancelled(THIS_YEAR, '%'),
		'offerings_cancelled_LY': inst_led_queries.offerings_cancelled(LAST_YEAR, course_code),
		'offerings_cancelled_TY': inst_led_queries.offerings_cancelled(THIS_YEAR, course_code),
		'top_5_depts': inst_led_queries.top_5_depts(lang, THIS_YEAR, course_code),
		'top_5_classifs': inst_led_queries.top_5_classifs(THIS_YEAR, course_code),
		'avg_class_size_overall_LY': inst_led_queries.avg_class_size(LAST_YEAR, '%'),
		'avg_class_size_overall_TY': inst_led_queries.avg_class_size(THIS_YEAR, '%'),
		'avg_class_size_LY': inst_led_queries.avg_class_size(LAST_YEAR, course_code),
		'avg_class_size_TY': inst_led_queries.avg_class_size(THIS_YEAR, course_code),
		'avg_no_shows_overall_LY': round(inst_led_queries.avg_no_shows(LAST_YEAR, '%'), 1),
		'avg_no_shows_overall_TY': round(inst_led_queries.avg_no_shows(THIS_YEAR, '%'), 1),
		'avg_no_shows_LY': round(inst_led_queries.avg_no_shows(LAST_YEAR, course_code), 1),
		'avg_no_shows_TY': round(inst_led_queries.avg_no_shows(THIS_YEAR, course_code), 1)
	}
	return render_template('instructor-led.html', pass_dict=pass_dict)


# Charts not yet implemented
@dashboards.route('/departmental')
def departmental():
	return render_template('departmental.html')


# Charts not yet implemented
@dashboards.route('/online')
def online():
	return render_template('online.html')
