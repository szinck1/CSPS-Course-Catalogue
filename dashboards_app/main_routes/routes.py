from flask import Blueprint, render_template, redirect, url_for, session
from flask_babel import gettext

main = Blueprint('main', __name__)


@main.route('/')
def index():
	return render_template('index.html')


@main.route('/about')
def about():
	return render_template('about.html')


# Possbile way to have /en/url and /fr/url and have bilingual urls
@main.route('/<lang>/')
def language(lang):
	session['lang'] = lang
	mars = gettext('Hello')
	return render_template('index.html')
