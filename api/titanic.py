from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from model.titanic import TitanicModel

titanic_api = Blueprint('titanic_api', __name__, url_prefix='/api/titanic')
api = Api(titanic_api)

class TitanicAPI:
    class _Predict(Resource):
        def post(self):
            data = request.get_json()
            required_fields = ['pclass', 'sex', 'age', 'sibsp', 'parch', 'fare', 'embarked', 'alone']
            
            # Validate input
            if not all(field in data for field in required_fields):
                return {"error": "Missing required fields", "required_fields": required_fields}, 400
            
            # Convert user input to expected format
            passenger = {
                'pclass': int(data['pclass']),
                'sex': 'male' if data['sex'].lower() == 'male' else 'female',
                'age': float(data['age']),
                'sibsp': int(data['sibsp']),
                'parch': int(data['parch']),
                'fare': float(data['fare']),
                'embarked': data['embarked'].upper(),
                'alone': bool(data['alone'])
            }
            
            titanicModel = TitanicModel.get_instance()
            response = titanicModel.predict(passenger)

            # Ensure response is a JSON-serializable dictionary
            return jsonify(response)  # Make sure it's a dict, not a Response object!

    api.add_resource(_Predict, '/predict')
