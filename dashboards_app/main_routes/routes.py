from flask import Blueprint, redirect, render_template, session, url_for

main = Blueprint('main', __name__)


@main.route('/')
def index():
	return render_template('index.html')


@main.route('/about')
def about():
	return render_template('about.html')


# Endpoint for button to switch language
@main.route('/switch-lang')
def switch_lang():
	if 'lang' in session and session['lang'] == 'en':
		return redirect(url_for('main.index', lang='fr'))
	return redirect(url_for('main.index', lang='en'))
