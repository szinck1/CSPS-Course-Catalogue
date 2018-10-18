# TODO
# Add requirements.txt
# Add French
# Speed: Code in vanilla JS to avoid importing jQuery

from flask import Flask, flash, redirect, render_template, request, session, url_for
import my_forms
from highcharts import inst_led

app = Flask(__name__)
app.config['DEBUG'] = True


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
		return redirect(url_for('inst_led_dash'))
	return render_template('form.html', form=form, title="Dashboard Parameters", button_val="Go")


# need pass in course code chosen in route above via query string
@app.route('/inst-led-dash')
def inst_led_dash():
	mars = inst_led.top_5_depts('Big Data')
	return render_template('instructor-led.html', mars=mars)


@app.route('/online')
def online():
	return render_template('online.html')


if __name__ == '__main__':
	app.run()
