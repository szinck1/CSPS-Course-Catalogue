from flask import Blueprint, jsonify, render_template, request
from catalogue_app import auth
from catalogue_app.config import Config
from catalogue_app.db import query_mysql

# Instantiate blueprint
api = Blueprint('api', __name__)


@api.route('/api/', methods=['GET', 'POST'])
@auth.login_required
def main():
	return render_template('api.html')


@api.route('/api/v1/get-courses/', methods=['GET', 'POST'])
@auth.login_required
def getcourses():
	lang = "en"
	table_year = 'lsr' + Config.THIS_YEAR # TODO - axcept mutliple years
	where = ' where 1=1 ' #Lazy trick, will rewrite as we go along
	desc = ''
	desc_join = ''
	
	### Language
	if "lang" in request.args:
		if request.args["lang"] == "fr":
			lang = "fr"
			title_field = " {0}.course_title_fr".format(table_year)
		else:
			title_field = " {0}.course_title_en".format(table_year)
	else:
		title_field = " {0}.course_title_en, course_title_fr ".format(table_year)
	
	### Title specific search
	if "title-text" in request.args: # May need to modify to only search appropriate language if lang is specified. Right now searches both lang titles
		txt = request.args['title-text'].replace("'","\\'").lower()
		where += " and (LOWER(course_title_en) like '%" + txt + "%' or LOWER(course_title_fr) like '%" + txt + "%') " ### DB is formated so LOWER() is necessary. May cause some overhead.
	
	### Specific course code
	if "course-code" in request.args:
		cc = request.args['course-code'].replace("'","\\'") 
		where += " and {0}.course_code='" + cc + "'".format(table_year)
	
	### Add descriptions or not
	if "descriptions" in request.args:
		if request.args["descriptions"].lower() == "true":
			desc = ', CONVERT(CAST(product_info.course_description as BINARY) using utf8)'
			desc_join = ' left join product_info on {0}.course_code = product_info.course_code '.format(table_year)
	
	# if year in request.args ### TO-DO, Maybe - current || last || all ?
	query = """
		SELECT DISTINCT {1}.course_code, {0} {3}
		FROM {1}
		{4}
		{2}
		ORDER BY 1 ASC;
	""".format(title_field,table_year, where,desc, desc_join )
	
	results = query_mysql(query)
	# Use flask.jsonify rather as it includes MIME type in response
	# json.dumps does not
	return jsonify(results)
