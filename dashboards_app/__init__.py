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

from dashboards_app import routes
