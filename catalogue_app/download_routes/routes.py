import csv
import datetime
from io import StringIO
from flask import Blueprint, make_response
from catalogue_app import auth
# from catalogue_app.download_routes.queries import download_queries

# Instantiate blueprint
downloads = Blueprint('downloads', __name__)


@downloads.route('/download-general')
@auth.login_required
def download_general():
	
	
	csvList = [
		[1, 2, 3],
		[4, 5, 6]
	]
	
	si = StringIO()
	cw = csv.writer(si)
	cw.writerows(csvList)
	
	output = make_response(si.getvalue())
	output.headers["Content-Disposition"] = "attachment; filename=export.csv"
	output.headers["Content-type"] = "text/csv"
	return output
	
	
	
	
	
	
	
	#timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#	return send_file(si.getvalue(),
#					 as_attachment=True,
#					 attachment_filename='thicc {0}.txt'.format(timestamp),
#					 mimetype='text/csv',
#					 # Prevent caching
#					 cache_timeout=-1)

					 
					 
					 
					 
					 
# Need to read through all docs, ensure doing properly
# Ensure headers like attachment and meme type
	# use curl to check if send_file options take care of headers


# Push tonight? ;)
