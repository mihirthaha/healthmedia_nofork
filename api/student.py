from flask import Blueprint, jsonify
from flask_restful import Api, Resource
import random

student_api = Blueprint('student_api', __name__, url_prefix='/api')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(student_api)

class StudentAPI:
    @staticmethod
    def get_student(name):
        students = {
            "Gavin": {
                "name": "Gavin",
                "age": 17,
                "major": "Nuclear Physicist",
                "university": "MIT and Harvard"
            },
            "Kush": {
                "name": "Kush",
                "age": 15,
                "major": "Biologist",     
                "university": "UCS"
            },
            "Trevor": {
                "name": "Trevor",
                "age": 17,
                "major": "Philanthropy",
                "university": "UCSB"
            },
            "Wyatt": {
                "name": "Wyatt",
                "age": 16,
                "major": "Finance",
                "university": "Utah State"
            },
             "Thomas": {
                "name": "Thomas",
                "age": 17,
                "major": "Biology",
                "university": "UCB"
            },
        }
        return students.get(name)
        
    class _Gavin(Resource):
        def get(self):
            # Use the helper method to get Jeff's details
            gavin_details = StudentAPI.get_student("Gavin")
            return jsonify(gavin_details)
        
    class _Trevor(Resource):
        def get(self):
            # Use the helper method to get Jeff's details
            trevor_details = StudentAPI.get_student("Trevor")
            return jsonify(trevor_details)
    
    class _Wyatt(Resource):
        def get(self):
            # Use the helper method to get Jeff's details
            wyatt_details = StudentAPI.get_student("Wyatt")
            return jsonify(wyatt_details)
        
    class _Kush(Resource):
        def get(self):
            # Use the helper method to get Jeff's details
            kush_details = StudentAPI.get_student("Kush")
            return jsonify(kush_details)
    class _Thomas(Resource):
        def get(self):
            # Use the helper method to get Jeff's details
            thomas_details = StudentAPI.get_student("Thomas")
            return jsonify(thomas_details)

    class _Bulk(Resource):
        def get(self):
            # Use the helper method to get both John's and Jeff's details
            gavin_details = StudentAPI.get_student("Gavin")
            trevor_details = StudentAPI.get_student("Trevor")
            wyatt_details = StudentAPI.get_student("Wyatt")
            kush_details = StudentAPI.get_student("Kush")
            thomas_details = StudentAPI.get_student("Thomas")
            return jsonify({"students": [gavin_details, trevor_details, wyatt_details, kush_details, thomas_details]})

    # Building REST API endpoints
    api.add_resource(_Gavin, '/student/gavin')
    api.add_resource(_Trevor, '/student/trevor')
    api.add_resource(_Wyatt, '/student/wyatt')
    api.add_resource(_Kush, '/student/kush')
    api.add_resource(_Thomas, '/student/thomas')
    api.add_resource(_Bulk, '/students')

# Instantiate the StudentAPI to register the endpoints
student_api_instance = StudentAPI()