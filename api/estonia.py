from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from model.estonia import EstoniaModel


estonia_api = Blueprint('estonia_api', __name__, url_prefix='/api/estonia')
api = Api(estonia_api)

class EstoniaAPI:
    class _Predict(Resource):
        def post(self):
            data = request.get_json()
            required_fields = ['Sex', 'Age', 'Category', 'Country']
            if not all(field in data for field in required_fields):
                return {"error": "Missing required fields", "required_fields": required_fields}, 400
            passenger = {
                'Sex': data['Sex'],
                'Age': float(data['Age']),
                'Category': data['Category'],
                'Country': data['Country']
            }
            estoniaModel = EstoniaModel.get_instance()
            response = estoniaModel.predict(passenger)
            return jsonify(response)
    
    api.add_resource(_Predict, '/predict')
