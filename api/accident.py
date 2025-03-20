from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from model.accident import AccidentModel

accident_api = Blueprint('accident_api', __name__, url_prefix='/api/accident')
api = Api(accident_api)

class AccidentAPI:
    class _Predict(Resource):
        def post(self):
            data = request.get_json()
            required_fields = ['Gender', 'Speed_of_Impact', 'Helmet_Used', 'Seatbelt_Used']
            
            if not all(field in data for field in required_fields):
                return {"error": "Missing required fields", "required_fields": required_fields}, 400
            
            accident_data = {
                'Gender': data['Gender'],
                'Speed_of_Impact': float(data['Speed_of_Impact']) if not isinstance(data['Speed_of_Impact'], float) else data['Speed_of_Impact'],
                'Helmet_Used': data['Helmet_Used'],
                'Seatbelt_Used': data['Seatbelt_Used']
            }

            accidentModel = AccidentModel.get_instance()
            response = accidentModel.predict(accident_data)
            
            return jsonify(response)
    
    api.add_resource(_Predict, '/predict')
