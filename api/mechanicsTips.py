from flask import Blueprint, request, jsonify, current_app, Response, g
from flask_restful import Api, Resource  # used for REST API building
from __init__ import app
from api.jwt_authorize import token_required
from model.mechanicsTips import MechanicsTip
from datetime import datetime  # Import datetime

# Create a Blueprint for mechanicsTips
mechanicsTips_api = Blueprint('mechanicsTips_api', __name__, url_prefix='/api')

# Initialize the Api object with the Blueprint
api = Api(mechanicsTips_api)

class MechanicsTipsAPI:
    """
    Define the API CRUD endpoints for the MechanicsTips model.
    There are four operations that correspond to common HTTP methods:
    - post: create a new tip
    - get: read tips
    - put: update a tip
    - delete: delete a tip
    """
    class _CRUD(Resource):
        @token_required()
        def post(self):
            current_user = g.current_user  # Access current request's user
            data = request.get_json()

            if "make" not in data or "model" not in data or "issue" not in data or "tip" not in data:
                return Response("{'message': 'Missing required fields'}", 400)

            # Create a new MechanicsTip object
            tip = MechanicsTip(current_user.id, data['make'], data['model'], data.get('year'), data['issue'], data['tip'])
            tip.create()

            # Return response to the client
            return jsonify(tip.read())

        def get(self):
            tips = MechanicsTip.query.all()

            if tips is None:
                return Response("{'message': 'Tips not found'}", 404)

            # Return response to the client
            return jsonify([tip.read() for tip in tips])

        @token_required()
        def put(self):
            current_user = g.current_user
            data = request.get_json()
            tip = MechanicsTip.query.get(data['id'])

            if tip is None:
                return Response("{'message': 'Tip not found'}", 404)

            tip.make = data.get('make', tip.make)
            tip.model = data.get('model', tip.model)
            tip.year = data.get('year', tip.year)
            tip.issue = data.get('issue', tip.issue)
            tip.tip = data.get('tip', tip.tip)
            tip.update()

            return jsonify(tip.read())

        @token_required()
        def delete(self):
            current_user = g.current_user
            data = request.get_json()
            tip = MechanicsTip.query.get(data['id'])

            if tip is None:
                return Response("{'message': 'Tip not found'}", 404)

            tip.delete()
            return jsonify({"message": "Tip deleted"})

    api.add_resource(_CRUD, '/mechanicsTips')  # Add CRUD resource to the API
