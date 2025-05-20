from flask import Blueprint, request, jsonify
import pandas as pd

# Create a Blueprint
length_bp = Blueprint("length", __name__)

# Load the correct CSV file
data = pd.read_csv("length.csv")

@length_bp.route("/predict", methods=["GET"])
def predict_engagement():
    try:
        video_length = int(request.args.get("video_length_seconds"))
        closest_row = data.iloc[(data['video_length_seconds'] - video_length).abs().argmin()]
        
        result = {
            "input_length": video_length,
            "closest_match_length": int(closest_row["video_length_seconds"]),
            "predicted_engagement": closest_row["engagement_quality"]
        }
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 400