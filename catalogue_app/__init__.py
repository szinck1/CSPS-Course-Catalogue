import os
from flask import Flask, g, request, session
from flask_babel import Babel
from catalogue_app.config import Debug
import mysql.connector


# Declare dictionary as app variable for memoization (stopgap solution before implementing Redis)
memo_dict = {}


# Instantiate plugins
babel = Babel()


# Connection to db to store in g
def get_db(local=True):
	if local:
		return mysql.connector.connect(host='localhost',
									   user='admin',
									   password='Newton11',
									   database='csps_dashboards')
	else:
		return mysql.connector.connect(host=os.environ.get('DB_HOST'),
									   user=os.environ.get('DB_USER'),
									   password=os.environ.get('DB_PASSWORD'),
									   database=os.environ.get('DB_DATABASE_NAME'))


# Application factory
def create_app(config_class=Debug):
	app = Flask(__name__)
	app.config.from_object(config_class)
	
	# Add Python's internal func 'zip' to Jinja2
	app.jinja_env.filters['zip'] = zip
	
	# Register plugins
	babel.init_app(app)
	
	# Register blueprints
	from catalogue_app.course_routes.routes import course
	from catalogue_app.main_routes.routes import main
	app.register_blueprint(course)
	app.register_blueprint(main)
	
	
	# Set language
	@app.before_request
	def get_lang():
		# Use if statements to avoid directly passing user input to code
		if 'lang' in request.args:
			if request.args['lang'] == 'fr':
				session['lang'] = 'fr'
			# If 'en'/junk/nothing is passed, default to en
			else:
				session['lang'] = 'en'
	
	
	@babel.localeselector
	def get_locale():
		return session.get('lang', 'en')
	
	
	@app.before_request
	def before_request():
		g.db = get_db(local=True)
	
	
	@app.teardown_request
	def teardown_request(exception):
		if hasattr(g, 'db'):
			g.db.close()
	
	return app
