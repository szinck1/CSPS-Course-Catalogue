from flask import Flask, render_template, request
from flask_httpauth import HTTPBasicAuth
from flask_babel import Babel
from catalogue_app.config import Config

# Declare dictionary as app variable for memoization
memo_dict = {}

# Instantiate login
auth = HTTPBasicAuth()
users = {
    Config.BASIC_AUTH_USERNAME: Config.BASIC_AUTH_PASSWORD
}

# Instantiate Babel for bilingual text
babel = Babel()


# Create a function for handling 404: Page not found
def not_found(e):
	return render_template('not-found.html'), 404


# Application factory
def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(config_class)
	
	# Add Python's internal funcs 'any' and 'zip' to Jinja2
	app.jinja_env.globals.update(any=any) 
	app.jinja_env.filters['zip'] = zip
	
	# Register database
	from catalogue_app import db
	db.init_app(app)
	
	
	# Register plugins
	@auth.get_password
	def get_pw(username):
		if username in users:
			return users.get(username)
		return None
	babel.init_app(app)
	
	# Register error handlers
	app.register_error_handler(404, not_found)
	
	# Set language
	@babel.localeselector
	def get_locale():
		# Only allow 'en' and 'fr' to be passed to app
		return 'fr' if request.cookies.get('lang', None) == 'fr' else 'en'
	
	# Register blueprints
	from catalogue_app.main_routes.routes import main
	from catalogue_app.course_routes.routes import course
	from catalogue_app.api_routes.routes import api
	from catalogue_app.download_routes.routes import downloads
	app.register_blueprint(main)
	app.register_blueprint(course)
	app.register_blueprint(api)
	app.register_blueprint(downloads)
	return app
