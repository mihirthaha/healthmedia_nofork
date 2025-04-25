import pandas as pd
from flask import Blueprint, jsonify
from flask_restful import Api, Resource
from __init__ import app
import csv
import os

# Define the Blueprint
legoland_time_api = Blueprint('legoland_time_api', __name__, url_prefix='/api')
api = Api(legoland_time_api)

# CSV file path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POSTS_FILE = os.path.join(BASE_DIR, 'legoland_posts.csv')

# Resource to return all posts (as before)
from flask import make_response


# Make sure this function only returns data or (data, status_code)
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


class LegolandTimeAPI(Resource):
    def get(self):
        result = load_posts()
        if isinstance(result, tuple):
            return make_response(jsonify(result[0]), result[1])
        return jsonify(result)


class LegolandOptimal(Resource):
    def get(self):
        result = load_posts()
        if isinstance(result, tuple):
            return make_response(jsonify(result[0]), result[1])

        posts = result['posts']
        df = pd.DataFrame(posts)

        hourly_avg = df.groupby('time_of_day')['likes_views'].mean()
        optimal_hour = int(hourly_avg.idxmax())
        highest_avg = float(hourly_avg.max())

        return jsonify({
            "optimal_hour": optimal_hour,
            "average_likes_views_at_optimal_hour": highest_avg,
            "hourly_averages": hourly_avg.to_dict()
        })


# Map the resources to the endpoints
api.add_resource(LegolandTimeAPI, '/timeofdayposts')
api.add_resource(LegolandOptimal, '/optimaltime')


if __name__ == '__main__':
    app.run(debug=True)
