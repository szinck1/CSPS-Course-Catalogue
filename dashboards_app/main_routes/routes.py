from flask import Blueprint, render_template
from dashboards_app import babel

main = Blueprint('main', __name__)


# Set language
@babel.localeselector
def get_locale():
	# return 'fr'
	return 'en'


@main.route('/')
def index():
	return render_template('index.html')


@main.route('/about')
def about():
	return render_template('about.html')
