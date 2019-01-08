from flask import Blueprint, render_template
from catalogue_app import auth

main = Blueprint('main', __name__)


@main.route('/')
@auth.login_required
def splash():
	return render_template('splash.html')


@main.route('/index')
@auth.login_required
def index():
	return render_template('index.html')


@main.route('/about')
@auth.login_required
def about():
	return render_template('about.html')
