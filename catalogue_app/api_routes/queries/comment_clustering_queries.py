from flask import jsonify
from catalogue_app.db import query_mysql

def mars():
	return jsonify('lard')
