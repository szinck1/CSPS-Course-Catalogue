# TODO
# Add requirements.txt
# Add French
# Include MySQL db on GitHub?
# Speed:
	# Code in vanilla JS to avoid importing jQuery
	# If statement to only scripts when needed

from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_mysqldb import MySQL

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


@app.route('/instructor-led')
def instructor_led():
	return render_template('instructor-led.html')


@app.route('/online')
def online():
	return render_template('online.html')


if __name__ == '__main__':
	app.run()
