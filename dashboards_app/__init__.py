from flask import Flask
from flask_babel import Babel
from dashboards_app.config import Debug

# Instantiate plugins
babel = Babel()


# Application factory
def create_app(config_class=Debug):
	app = Flask(__name__)
	app.config.from_object(config_class)
	
	# Add Python's internal func 'zip' to Jinja2
	app.jinja_env.filters['zip'] = zip
	
	# Register plugins
	babel.init_app(app)
	
	# Register blueprints
	from dashboards_app.dashboard_routes.routes import dashboards
	from dashboards_app.main_routes.routes import main
	app.register_blueprint(dashboards)
	app.register_blueprint(main)
	
	return app
