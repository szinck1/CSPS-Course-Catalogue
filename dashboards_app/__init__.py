from flask import Flask
from config import Debug
import forms
import inst_led

# Instantiation and config
app = Flask(__name__)
app.config.from_object(Debug)

# Add Python's internal func 'zip' to Jinja2
app.jinja_env.filters['zip'] = zip

# Set global vars and make accessible by all templates
LAST_YEAR = app.config['LAST_YEAR']
THIS_YEAR = app.config['THIS_YEAR']


# from flask_babel import Babel
# babel = Babel(app)
# from flask import flash, redirect, render_template, request, session, url_for
