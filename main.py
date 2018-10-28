### CURRENT SPRINT ###
# Add requirements.txt
# Check results with real data


### BACKLOG ###
# Use blueprints
# Protect against SQL injection and XSS; remove use of '| safe'
# Add Google Analytics
# Add French; use if session['FR']?
	# Change language via button
	# Bilingual URLs as well
	# Open to XSS?
# Add drilldown
# Add (cumulative?) unique leaners
# Course catalogue: add description, add L1 data, add comments w/ 1-5 stars
# Add Online, Departmental
# Add dates and other options to Dashboard Parameters


from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_babel import Babel
from main_config import Debug
import my_forms
from highcharts import inst_led

# Instantiation and config
app = Flask(__name__)
babel = Babel(app)
# app.config.from_pyfile('main_config.py')
app.config.from_object(Debug)
# Add Python's internal func 'zip' to Jinja2
app.jinja_env.filters['zip'] = zip

# Set global vars and make accessible by all templates
LAST_YEAR = app.config['LAST_YEAR']
THIS_YEAR = app.config['THIS_YEAR']
@app.context_processor
def context_processor():
	return {'LAST_YEAR': LAST_YEAR.replace('_', '-'), 'THIS_YEAR': THIS_YEAR.replace('_', '-')}


@babel.localeselector
def get_locale():
	# return 'fr'
	return 'en'


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/about')
def about():
	return render_template('about.html')


@app.route('/departmental')
def departmental():
	return render_template('departmental.html')


@app.route('/instructor-led', methods=['GET', 'POST'])
def instructor_led():
	form = my_forms.CourseForm(request.form)
	if request.method == 'POST' and form.validate():
		course_title = form.course_title.data
		return redirect(url_for('inst_led_dash', course_title=course_title))
	return render_template('form.html', form=form, title="Dashboard Parameters", button_val="Go")


@app.route('/inst-led-dash')
def inst_led_dash():
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


@app.route('/online')
def online():
	return render_template('online.html')


if __name__ == '__main__':
	app.run()
