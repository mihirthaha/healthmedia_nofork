from flask import Blueprint, jsonify
from flask_restful import Api, Resource
from flask import Blueprint, request, jsonify
import requests

# Create a Blueprint for the VIN decoding functionality
vin_api = Blueprint('vin_api', __name__, url_prefix='/api')
api = Api(vin_api)

# Base URL for the NHTSA VIN decoding API
NHTSA_API_URL = "https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValues/"

class _DecodeVin(Resource):
    def post(self):
        # Parse the VIN from the request
        data = request.get_json()
        vin = data.get('vin')

        # Validate the VIN
        if not vin:
            return jsonify({"error": "VIN is required"}), 400

        if len(vin) != 17:
            return jsonify({"error": "VIN must be 17 characters long"}), 400

        # Send the request to the NHTSA API
        response = requests.get(f"{NHTSA_API_URL}{vin}?format=json")
        
        if response.status_code != 200:
            return jsonify({"error": "Failed to retrieve data from the NHTSA API"}), 500

        # Parse and return the response data
        vin_data = response.json()
        return jsonify(vin_data)

# Add the resource to the API
api.add_resource(_DecodeVin, '/decode-vin')
vin_api_instance = _DecodeVin()
