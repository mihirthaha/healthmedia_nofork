from flask import Blueprint, request, jsonify
import pandas as pd
import os

# Create a Blueprint
length_bp = Blueprint("length", __name__, url_prefix="/api/lengths")

# Load CSV safely (relative to this file's locations)
csv_path = os.path.join(os.path.dirname(__file__), "../length.csv")
data = pd.read_csv(csv_path)

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
