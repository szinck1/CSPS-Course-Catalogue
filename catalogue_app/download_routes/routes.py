import datetime
from flask import Blueprint, make_response
from flask_babel import gettext
from catalogue_app import auth
from catalogue_app.download_routes.queries import download_queries

# Instantiate blueprint
downloads = Blueprint('downloads', __name__)


@downloads.route('/download-general')
@auth.login_required
def download_general():
	# Query raw data
	raw_data = download_queries.general_tab('S202')
	output = make_response(raw_data)
	# Add headers with filename and type
	filename = gettext('General Tab')
	timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	output.headers['Content-Disposition'] = 'attachment; filename={0} {1}.csv'.format(filename, timestamp)
	output.headers['Content-type'] = 'text/csv'
	return output


# Ensure validate user input, only create CSV for safe course codes
	# Simply produce CSV with BILINGUAL error message if junk is passed (test this)
# Push to Azure
