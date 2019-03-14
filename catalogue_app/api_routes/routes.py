from flask import Blueprint, jsonify
from catalogue_app import auth
from catalogue_app.api_routes.queries import comment_clustering_queries

# Instantiate blueprint
api = Blueprint('api', __name__)


@api.route('/api/v1/lda/<string:course_code>')
@auth.login_required
def lda(course_code):
	clusters = comment_clustering_queries.get_clusters(course_code)
	# Same as Python built-in json.dumps but also creates response and
	# adds MIME type
	return jsonify(clusters)
