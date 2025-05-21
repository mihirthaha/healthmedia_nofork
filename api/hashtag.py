from flask import Blueprint, jsonify, request
import csv

# Define the blueprint for the hashtag API
hashtag_api = Blueprint('hashtag_api', __name__, url_prefix='/api')

# Route to return all hashtags with likes, views, and score
@hashtag_api.route('/average_likes', methods=['GET'])
def average_likes_from_csv():
    results = []
    try:
        with open('hashtags.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                results.append({
                    'hashtag': row['Hashtag'].strip(),
                    'average_likes': round(float(row['AverageLikes']), 2),
                    'estimated_views': round(float(row['EstimatedViews'])),
                    'hashtag_success_score': int(row['HashtagSuccessScore'])
                })
    except FileNotFoundError:
        return jsonify({'error': 'hashtags.csv file not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify(results), 200

# Route to return a single hashtag's metrics
@hashtag_api.route('/average_likes/<hashtag>', methods=['GET'])
def get_hashtag_avg_likes(hashtag):
    try:
        with open('hashtags.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['Hashtag'].strip().lower() == hashtag.lower():
                    return jsonify({
                        'hashtag': hashtag,
                        'average_likes': round(float(row['AverageLikes']), 2),
                        'estimated_views': round(float(row['EstimatedViews'])),
                        'hashtag_success_score': int(row['HashtagSuccessScore'])
                    }), 200
        return jsonify({'message': f'Hashtag "{hashtag}" not found'}), 404
    except FileNotFoundError:
        return jsonify({'error': 'hashtags.csv file not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# POST route to analyze input hashtags and return aggregated metrics
@hashtag_api.route('/hashtag', methods=['POST'])
def analyze_hashtags_from_csv():
    data = request.get_json()
    if not data or 'hashtags' not in data:
        return jsonify({'error': 'No hashtags provided'}), 400

    input_tags = [tag.strip().lower().lstrip('#') for tag in data['hashtags'].split()]
    total_likes = 0
    total_views = 0
    total_score = 0
    count = 0

    try:
        with open('hashtags.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                tag = row['Hashtag'].strip().lower()
                if tag in input_tags:
                    total_likes += float(row['AverageLikes'])
                    total_views += float(row['EstimatedViews'])
                    total_score += int(row['HashtagSuccessScore'])
                    count += 1
    except FileNotFoundError:
        return jsonify({'error': 'hashtags.csv file not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    response = {
        'average_likes': round(total_likes / count, 2) if count else 0,
        'total_estimated_views': round(total_views),
        'average_hashtag_success_score': round(total_score / count, 1) if count else 0
    }

    return jsonify(response), 200
