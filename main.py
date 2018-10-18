# TODO
# Add requirements.txt
# Add French
# Speed:
	# Code in vanilla JS to avoid importing jQuery
	# If statement to only scripts when needed

from flask import Flask, flash, redirect, render_template, request, session, url_for
import my_forms

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
		return '<h1>' + course_title + '</h1>'
	
	return render_template('form.html', form=form, title="Login", button_val="Login")


@app.route('/online')
def online():
	return render_template('online.html')


if __name__ == '__main__':
	app.run()
