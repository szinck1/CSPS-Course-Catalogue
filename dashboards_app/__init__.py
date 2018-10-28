from flask import Flask
from flask_babel import Babel
from dashboards_app.config import Debug

# Instantiation and config
app = Flask(__name__)
app.config.from_object(Debug)
babel = Babel(app)

# Add Python's internal func 'zip' to Jinja2
app.jinja_env.filters['zip'] = zip

# Make LAST_YEAR and THIS_YEAR available to all modules
LAST_YEAR = app.config['LAST_YEAR']
THIS_YEAR = app.config['THIS_YEAR']

# Register blueprints
from dashboards_app.dashboard_routes.routes import dashboards
from dashboards_app.main_routes.routes import main
app.register_blueprint(dashboards)
app.register_blueprint(main)
