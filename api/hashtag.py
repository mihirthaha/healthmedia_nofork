from flask import Blueprint, jsonify, request
import csv

# Define the blueprint for the hashtag API
hashtag_api = Blueprint('hashtag_api', __name__, url_prefix='/api')

# Route to return all hashtags and their average likes from the CSV
@hashtag_api.route('/average_likes', methods=['GET'])
def average_likes_from_csv():
    results = []
    try:
        with open('hashtags.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                hashtag = row['Hashtag'].strip()
                likes = float(row['AverageLikes'])
                results.append({
                    'hashtag': hashtag,
                    'average_likes': round(likes, 2)
                })
    except FileNotFoundError:
        return jsonify({'error': 'hashtags.csv file not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify(results), 200

# Route to return a single hashtag's average likes
@hashtag_api.route('/average_likes/<hashtag>', methods=['GET'])
def get_hashtag_avg_likes(hashtag):
    try:
        with open('hashtags.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['Hashtag'].strip().lower() == hashtag.lower():
                    likes = float(row['AverageLikes'])
                    return jsonify({
                        'hashtag': hashtag,
                        'average_likes': round(likes, 2)
                    }), 200
        return jsonify({'message': f'Hashtag "{hashtag}" not found'}), 404
    except FileNotFoundError:
        return jsonify({'error': 'hashtags.csv file not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to handle hashtag analysis from the frontend
@hashtag_api.route('/api/hashtag', methods=['POST'])
def analyze_hashtags_from_csv():
    data = request.get_json()
    if not data or 'hashtags' not in data:
        return jsonify({'error': 'No hashtags provided'}), 400

    input_tags = [tag.strip().lower().lstrip('#') for tag in data['hashtags'].split()]
    total_likes = 0
    count = 0

    try:
        with open('hashtags.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                tag = row['Hashtag'].strip().lower()
                if tag in input_tags:
                    total_likes += float(row['AverageLikes'])
                    count += 1
    except FileNotFoundError:
        return jsonify({'error': 'hashtags.csv file not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    average = round(total_likes / count) if count > 0 else 0
    return jsonify({'views': average}), 200
