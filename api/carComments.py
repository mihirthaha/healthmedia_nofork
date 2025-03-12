import jwt
from flask import Blueprint, request, jsonify, current_app, Response, g
from flask_restful import Api, Resource  # used for REST API building
from datetime import datetime
from __init__ import app
from api.jwt_authorize import token_required
from model.carComments import CarComments
import base64
import json

carComments_api = Blueprint('carComments_api', __name__, url_prefix='/api')

api = Api(carComments_api)

class CarCommentsAPI:

    class _CRUD(Resource):
        @token_required()
        def post(self):
            # Obtain the current user from the token required setting in the global context
            current_user = g.current_user
            # Obtain the request data sent by the RESTful client API
            data = request.get_json()

            if "content" not in data or "post_id" not in data:
                return Response("{'message': 'Missing required fields'}", 400)

            # Create a new post object using the data from the request
            comment = CarComments(current_user.id, data['post_id'], data['content'])
            # Save the post object using the Object Relational Mapper (ORM) method defined in the model
            comment.create()

            return jsonify(comment.read())
        
        def get(self):

            comments = CarComments.query.all()

            if comments is None:
                return Response("{'message': 'Comment not found'}", 404)
            
            # Return response to the client in JSON format, converting Python dictionaries to JSON format
            return jsonify([comment.read() for comment in comments])

        @token_required()
        def put(self):
            # Obtain the current user
            current_user = g.current_user
            # Obtain the request data
            data = request.get_json()
            # Find the current post from the database table(s)
            comment = CarComments.query.get(data['id'])
            # Update the comment
            comment._content = data['content']
            # Save the post
            comment.update()
            # Return response
            return jsonify(comment.read())

        @token_required()
        def delete(self):
            # Obtain the current user
            current_user = g.current_user
            # Obtain the request data
            data = request.get_json()
            # Find the current post from the database table(s)
            comment = CarComments.query.get(data['id'])
            # Delete the post using the ORM method defined in the model
            comment.delete()
            # Return response
            return jsonify({"message": "Post deleted"})

    api.add_resource(_CRUD, '/carComment')