from flask import Blueprint, current_app, redirect, render_template, request, url_for
from dashboards_app.dashboard_routes.forms import CourseForm
import dashboards_app.dashboard_routes.inst_led as inst_led

dashboards = Blueprint('dashboards', __name__)

# Make LAST_YEAR and THIS_YEAR available to all templates
@dashboards.context_processor
def context_processor():
	LAST_YEAR = current_app.config.get('LAST_YEAR')
	THIS_YEAR = current_app.config.get('THIS_YEAR')
	return {'LAST_YEAR': LAST_YEAR.replace('_', '-'), 'THIS_YEAR': THIS_YEAR.replace('_', '-')}


# Form to get query parameters from user
@dashboards.route('/instructor-led', methods=['GET', 'POST'])
def instructor_led():
	form = CourseForm(request.form)
	if request.method == 'POST' and form.validate():
		course_title = form.course_title.data
		return redirect(url_for('dashboards.inst_led_dash', course_title=course_title))
	return render_template('form.html', form=form, title="Dashboard Parameters", button_val="Go")


# Run queries and pass to + render template
@dashboards.route('/inst-led-dash')
def inst_led_dash():
	
	LAST_YEAR = current_app.config.get('LAST_YEAR')
	THIS_YEAR = current_app.config.get('THIS_YEAR')
	
	# Get arguments from query string
	course_title = request.args['course_title']
	
	# Run queries and save in dict to be passed to templates
	pass_dict = {
		'course_code': inst_led.course_code(THIS_YEAR, course_title),
		'general_info_LY': inst_led.general_info(LAST_YEAR, course_title),
		'general_info_TY': inst_led.general_info(THIS_YEAR, course_title),
		'offerings_per_region': inst_led.offerings_per_region(THIS_YEAR, course_title),
		'offerings_per_lang': inst_led.offerings_per_lang(THIS_YEAR, course_title),
		'offerings_cancelled_overall_LY': inst_led.offerings_cancelled(LAST_YEAR, '%'),
		'offerings_cancelled_overall_TY': inst_led.offerings_cancelled(THIS_YEAR, '%'),
		'offerings_cancelled_LY': inst_led.offerings_cancelled(LAST_YEAR, course_title),
		'offerings_cancelled_TY': inst_led.offerings_cancelled(THIS_YEAR, course_title),
		'top_5_depts': inst_led.top_5_depts(THIS_YEAR, course_title),
		'top_5_classifs': inst_led.top_5_classifs(THIS_YEAR, course_title),
		'avg_class_size_overall_LY': inst_led.avg_class_size(LAST_YEAR, '%'),
		'avg_class_size_overall_TY': inst_led.avg_class_size(THIS_YEAR, '%'),
		'avg_class_size_LY': inst_led.avg_class_size(LAST_YEAR, course_title),
		'avg_class_size_TY': inst_led.avg_class_size(THIS_YEAR, course_title),
		'avg_no_shows_overall_LY': round(inst_led.avg_no_shows(LAST_YEAR, '%'), 1),
		'avg_no_shows_overall_TY': round(inst_led.avg_no_shows(THIS_YEAR, '%'), 1),
		'avg_no_shows_LY': round(inst_led.avg_no_shows(LAST_YEAR, course_title), 1),
		'avg_no_shows_TY': round(inst_led.avg_no_shows(THIS_YEAR, course_title), 1)
	}
	return render_template('instructor-led.html', pass_dict=pass_dict)


# Not yet implemented
@dashboards.route('/departmental')
def departmental():
	return render_template('departmental.html')


# Not yet implemented
@dashboards.route('/online')
def online():
	return render_template('online.html')
