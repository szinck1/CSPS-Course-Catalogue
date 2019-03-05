import datetime
from io import BytesIO
from flask import Blueprint, send_file
from catalogue_app import auth
from catalogue_app.download_routes.queries import download_queries

# Instantiate blueprint
downloads = Blueprint('downloads', __name__)


@downloads.route('/download-blimp')
@auth.login_required
def download_blimp():
	buffer = BytesIO()
	my_text = b"Hi Fatso you're so thin!"
	#my_text = bytes(my_text)
	buffer.write(my_text)
	buffer.seek(0)
	
	#timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	
	return send_file(buffer,
					 as_attachment=True,
					 attachment_filename='thicc.txt',
					 mimetype='text/plain',
					 cache_timeout=-1)
