import jwt
from flask import Blueprint, request, jsonify, current_app, Response, g
from flask_restful import Api, Resource  # used for REST API building
from datetime import datetime
from __init__ import app
from api.jwt_authorize import token_required
from model.userCars import UserCars
import json

"""
This Blueprint object is used to define APIs for the Post model.
- Blueprint is used to modularize application files.
- This Blueprint is registered to the Flask app in main.py.
"""
userCars_api = Blueprint('userCars_api', __name__, url_prefix='/api')

"""
The Api object is connected to the Blueprint object to define the API endpoints.
- The API object is used to add resources to the API.
- The objects added are mapped to code that contains the actions for the API.
- For more information, refer to the API docs: https://flask-restful.readthedocs.io/en/latest/api.html
"""
api = Api(userCars_api)

class CarPostAPI:
    """
    Define the API CRUD endpoints for the Post model.
    There are four operations that correspond to common HTTP methods:
    - post: create a new post
    - get: read posts
    - put: update a post
    - delete: delete a post
    """
    class _CRUD(Resource):
        @token_required()
        def post(self):
            # Obtain the current user from the token required setting in the global context
            current_user = g.current_user
            # Obtain the request data sent by the RESTful client API
            data = request.get_json()

            if "make" not in data or "model" not in data or  "engine_type" not in data or "year" not in data:
                return Response("{'message': 'Missing required fields'}", 400)

            # Create a new post object using the data from the request
            post = UserCars(current_user.id, data["make"], data["model"], data["year"], data["engine_type"], data["trim"], data["color"], data["vin"]) 
            # Save the post object using the Object Relational Mapper (ORM) method defined in the model
            post.create()

            # for base64_image in data['image_base64_table']:
            #     print(base64_image)
            #     carPostImage_base64_upload(base64_image, post.id, )

            # Return response to the client in JSON format, converting Python dictionaries to JSON format
            return jsonify(post.read())
        @token_required()
        def get(self):
            # """
            # Retrieve all cars associated with the authenticated user.

            # Returns:
            #     JSON response with a list of car dictionaries.
            # """
            current_user = g.current_user

            return jsonify([car.read() for car in UserCars.query.filter_by(_uid=current_user.id).all()])

        @token_required()
        def put(self):
            # Obtain the current user
            current_user = g.current_user
            # Obtain the request data
            data = request.get_json()
            # Find the current post from the database table(s)
            car = UserCars.query.get(data['id'])
            # Update the car
            car._make = data["make"]
            car._color = data["color"]
            car._engine_type = data["engine_type"]
            car._model = data["model"]
            car._year = data["year"]
            car._trim = data["trim"]
            car._vin = data["vin"]
            # Save the car
            car.update()
            # Return response
            return jsonify(car.read())

        @token_required()
        def delete(self):
            # Obtain the current user
            current_user = g.current_user
            # Obtain the request data
            data = request.get_json()
            # Find the current car from the database table(s)
            car = UserCars.query.get(data['id'])

            if car is None:
                return Response("{'message': 'Car not found'}", 404)

            if car._uid != current_user.id:
                return Response("{'message': 'Unauthorized'}", 401)
            # Delete the car using the ORM method defined in the model
            if car:
                car.delete()
            # Return response
                return jsonify({"message": "Car deleted"})
            else:
                return Response("{'message': 'Car not found'}", 404)

    """
    Map the _CRUD class to the API endpoints for /post.
    - The API resource class inherits from flask_restful.Resource.
    - The _CRUD class defines the HTTP methods for the API.
    """
    api.add_resource(_CRUD, '/userCars')