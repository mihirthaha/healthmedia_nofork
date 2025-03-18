from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from model.cancer import CancerModel

cancer_api = Blueprint('cancer_api', __name__, url_prefix='/api/cancer')
api = Api(cancer_api)

class CancerAPI:
    class _Predict(Resource):
        def post(self):
            data = request.get_json()
            required_fields = ['age', 'year']
            
            if not all(field in data for field in required_fields):
                return {"error": "Missing required fields", "required_fields": required_fields}, 400
            
            patient_data = {
                'age': float(data['age']) if not isinstance(data['age'], float) else data['age'],
                'year': int(data['year']) if not isinstance(data['year'], int) else data['year']
            }

            cancerModel = CancerModel.get_instance()
            response = cancerModel.predict(patient_data)

            return jsonify(response)

    api.add_resource(_Predict, '/predict')
