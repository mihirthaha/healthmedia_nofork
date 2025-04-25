import csv
from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource
from __init__ import app  # Ensure __init__.py initializes your Flask app

# Define the Blueprint
legoland_time_api = Blueprint('legoland_time_api', __name__, url_prefix='/api')

# Attach Flask-RESTful API to the Blueprint
api = Api(legoland_time_api)

# CSV file path
POSTS_FILE = '/home/mihirthaha/nighthawk/healthmedia_backend-1/api/legoland_posts.csv'


# Helper function to load posts from CSV
def load_posts():
    posts = []
    try:
        with open(POSTS_FILE, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    likes_views = int(row['likes/views'].replace(",", ""))
                    time_of_day = int(row['time_of_day'])
                    posts.append({
                        "url": row['url'],
                        "likes_views": likes_views,
                        "time_of_day": time_of_day
                    })
                except ValueError:
                    continue  # Skip malformed rows

        if not posts:
            return {"error": "No valid post data found."}, 404

        return {
            "total_posts": len(posts),
            "posts": posts
        }

    except Exception as e:
        return {"error": str(e)}, 500


# Define the Resource class
class LegolandTimeAPI(Resource):
    def get(self):
        result = load_posts()
        if isinstance(result, tuple):
            return jsonify(result[0]), result[1]
        return jsonify(result)


# Map the resource to the endpoint
api.add_resource(LegolandTimeAPI, '/posts')


if __name__ == '__main__':
   app.run(debug=True)
