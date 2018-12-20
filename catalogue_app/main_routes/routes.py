from flask import Blueprint, render_template
from catalogue_app import basic_auth

main = Blueprint('main', __name__)


@main.route('/')
@basic_auth.required
def index():
	return render_template('index.html')


@main.route('/about')
@basic_auth.required
def about():
	return render_template('about.html')
