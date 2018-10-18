# TODO
# Add requirements.txt
# Add French
# Include MySQL db on GitHub?
# Speed:
	# Code in vanilla JS to avoid importing jQuery
	# If statement to only scripts when needed

from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_mysqldb import MySQL
import my_forms

app = Flask(__name__)
mysql = MySQL(app)
app.config.from_pyfile('config.cfg')


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
	# Get list of courses currently in LSR
	query = "SELECT DISTINCT course_title FROM lsr ORDER BY 1 ASC;"
	cur = mysql.connection.cursor()
	with mysql.connection.cursor() as cur:
		x = cur.execute(query)
		y = cur.fetchall()
	#course_list = [val for tup in y for val in tup]
	# Use list to populate dropdown menu
	# form = my_forms.wtforms_dropdown(field_name='Course Code', my_list=course_list)
	form = my_forms.SkillsForm(request.form)
	
	return render_template('form.html', form=form, title="Sean", button_val="Go")
	
	
	
	
	
	
@app.route('/online')
def online():
	return render_template('online.html')


if __name__ == '__main__':
	app.run()
