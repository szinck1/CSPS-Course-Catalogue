from flask import Flask, jsonify, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class PassingStrings(Resource):
	"""Values returned from flask_restful will indicate
	   'Content-Type: application/json' in header by default.
	"""
	def get(self):
		"""Return JSON to GET request."""
		# Use jsonify??
		return {'Team': 'DIS'}
	
	
	def post(self):
		"""Allow user to pass JSON in POST request."""
		passed = request.get_json()
		return {'you sent': passed}, 201


class Square(Resource):
	def get(self, my_num):
		"""Square number passed in URL."""
		return my_num ** 2


# Add classes and their associated routes to app
api.add_resource(PassingStrings, '/api/team')
api.add_resource(Square, '/api/square/<int:my_num>')

if __name__ == '__main__':
	app.run(debug=True)
