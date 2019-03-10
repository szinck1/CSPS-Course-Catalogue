from flask import Blueprint
from catalogue_app import auth
from catalogue_app.api_routes.queries import comment_clustering_queries

# Instantiate blueprint
api = Blueprint('api', __name__)


@api.route('/api/v1/get-clusters')
@auth.login_required
def get_clusters():
	return comment_clustering_queries.mars()
