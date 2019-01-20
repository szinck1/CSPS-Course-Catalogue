import os

class Config:
	DEBUG = True
	LOAD_FROM_PICKLE = False
	LOCAL_DB = True
	LAST_YEAR = '2017_18'
	THIS_YEAR = '2018_19'
	BABEL_DEFAULT_LOCALE = 'en'
	# Load strings from environ vars to avoid storing in plaintext
	BASIC_AUTH_USERNAME = os.environ.get('BASIC_AUTH_USERNAME')
	BASIC_AUTH_PASSWORD = os.environ.get('BASIC_AUTH_PASSWORD')
	SECRET_KEY = os.environ.get('SECRET_KEY')
