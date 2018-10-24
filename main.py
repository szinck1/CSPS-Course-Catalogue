# For Friday, October 24 2018
# Add requirements.txt
# Add remaining charts in Instructor-Led

# Backlog
# Protect against SQL injection and XSS
# Add Google Analytics
# Add French; use if session['FR']?
	# Change language via button
	# Bilingual URLs as well
	# Open to XSS?
# Add global vars for fiscal year
# Add Online, Departmental
# Add drilldown


from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_babel import Babel, gettext
import my_forms
from highcharts import inst_led

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'meow123'
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
babel = Babel(app)


@babel.localeselector
def get_locale():
	if request.args.get('lang'):
		session['lang'] = request.args.get('lang')
	return session.get('lang', 'en')


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
	general_info = inst_led.general_info(course_title)
	top_5_depts = inst_led.top_5_depts(course_title)
	top_5_classifs = inst_led.top_5_classifs(course_title)
	offerings_per_region_j = inst_led.offerings_per_region(course_title)
	offerings_per_lang_j = inst_led.offerings_per_lang(course_title)
	avg_class_size_overall_2017 = inst_led.average_class_size('2017', '%')
	avg_class_size_overall_2018 = inst_led.average_class_size('2018', '%')
	avg_class_size_2017 = inst_led.average_class_size('2017', course_title)
	avg_class_size_2018 = inst_led.average_class_size('2018', course_title)
	
	return render_template('instructor-led.html', course_title=course_title,
												  general_info=general_info,
												  top_5_depts=top_5_depts,
												  top_5_classifs=top_5_classifs,
												  offerings_per_region_j=offerings_per_region_j,
												  offerings_per_lang_j=offerings_per_lang_j,
												  avg_class_size_overall_2017=avg_class_size_overall_2017,
												  avg_class_size_overall_2018=avg_class_size_overall_2018,
												  avg_class_size_2017=avg_class_size_2017,
												  avg_class_size_2018=avg_class_size_2018)


@app.route('/online')
def online():
	return render_template('online.html')


if __name__ == '__main__':
	app.run()
