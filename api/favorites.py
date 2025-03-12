from flask import Blueprint, request, jsonify, Response, g
from flask_restful import Api, Resource
from sqlalchemy.exc import SQLAlchemyError
from __init__ import db
from api.jwt_authorize import token_required
from model.listings import UserItem

# Create a Blueprint for the user item storage functionality
itemStore_api = Blueprint('itemStore_api', __name__, url_prefix='/api')
api = Api(itemStore_api)

class UserItemAPI:
    class _CRUD(Resource):
        @token_required()
        def post(self):
            """
            Store a new item name associated with the authenticated user.

            Request Body:
                {
                    "name": "<item_name>"
                }

            Returns:
                JSON response with the stored item details.
            """
            # Retrieve the current user from the context (via JWT or session)
            current_user = g.current_user

            if not current_user:
                return jsonify({"message": "User is not authenticated"}), 401

            # Parse the item name from the request
            data = request.get_json()
            item_name = data.get('name')

            if not item_name:
                return Response("{'message': 'Item name is required'}", status=400, mimetype='application/json')

            # Check if the item already exists for the user
            existing_item = UserItem.query.filter_by(name=item_name, user_id=current_user.id).first()
            if existing_item:
                return jsonify({"message": "Item already exists", "item": existing_item.read()})

            # Create a new UserItem object
            item_user_input = data.get('user_input')  # Extract user_input from the request
            new_item = UserItem(name=item_name, user_id=current_user.id, user_input=item_user_input)


            try:
                # Save the item to the database
                db.session.add(new_item)
                db.session.commit()
            except SQLAlchemyError as e:
                db.session.rollback()
                return Response(f"{{'message': 'Database error: {str(e)}'}}", status=500, mimetype='application/json')

            return jsonify(new_item.read())

        def get(self):
            """
            Retrieve all items associated with the user.

            Returns:
                JSON response with a list of item dictionaries.
            """
            # Query the database for items
            user_items = UserItem.query.all()

            if not user_items:
                return jsonify({"message": "No items found"}), 404

            # Prepare a JSON list of the user's items
            json_ready = [item.read() for item in user_items]

            return jsonify(json_ready)
        
        
        @token_required()
        def put(self):
            # Obtain the current user
            current_user = g.current_user
            # Obtain the request data
            data = request.get_json()
            # Find the current post from the database table(s)
            user_item = UserItem.query.get(data['id'])
            # Update the post
            user_item.user_input= data['user_input']
            # Save the post
            user_item.update(data['user_input'])
            # Return response
            return jsonify(user_item.read())
            
        def delete(self):
            """
            Delete an item by name.

            Request Body:
                {
                    "name": "<item_name>"
                }

            Returns:
                JSON response confirming deletion or an error message.
            """
            # Parse the item name from the request
            data = request.get_json()

            item_name = data.get('name')
            if not item_name:
                return Response("{'message': 'Item name is required for deletion'}", status=400, mimetype='application/json')

            # Find the item by name
            item = UserItem.query.filter_by(name=item_name).first()
            if not item:
                return Response(f"{{'message': 'Item with name {item_name} not found'}}", status=404, mimetype='application/json')

            try:
                # Delete the item record
                db.session.delete(item)
                db.session.commit()
                return jsonify({"message": f"Item '{item_name}' has been successfully deleted."})
            except SQLAlchemyError as e:
                db.session.rollback()
                return Response(f"{{'message': 'Database error: {str(e)}'}}", status=500, mimetype='application/json')

    api.add_resource(_CRUD, '/itemStore')
