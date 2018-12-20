import os

class Config:
	DEBUG = False
	LOAD_FROM_PICKLE = True
	SECRET_KEY = os.environ.get('SECRET_KEY')
	LAST_YEAR = '2017_18'
	THIS_YEAR = '2018_19'
	BABEL_DEFAULT_LOCALE = 'en'
