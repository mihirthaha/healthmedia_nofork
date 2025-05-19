from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from textblob import TextBlob
from collections import defaultdict
import random
import pandas as pd
import csv
import pandas as pd
from sklearn.linear_model import LinearRegression
from PIL import Image, ImageStat
import numpy as np
import os
from flask import request
from model.image import model, predict_likes_from_image, extract_image_features

db = SQLAlchemy()

# initialize a flask application (app)
app = Flask(__name__)
CORS(app, supports_credentials=True, origins='*')  # Allow all origins (*)

# Function to load comments from the CSV file
def get_comments_from_file():
    comments = []
    try:
        import os
        csv_path = os.path.join(os.path.dirname(__file__), 'api', 'legoland_comments_all_posts.csv')
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                comments.append(row['Comment'])  # Assuming 'Comment' is the correct column name
    except Exception as e:
        print(f"Error loading comments: {e}")
    return comments

# Function for sentiment analysis (mock)
def analyze_sentiment(comment):
    # This is where you would analyze the sentiment of the comment
    # For now, let's mock it to return a random sentiment score between -1 and 1
    return random.uniform(-1, 1)

# Add an API endpoint for sentiment analysis
@app.route('/api/sentiment', methods=['GET'])
def analyze_sentiment():
    try:
        # Load CSV file
        df = pd.read_csv('/home/mihirthaha/nighthawk/healthmedia_backend-1/api/legoland_comments_all_posts.csv')

        # Group comments by Post Shortcode
        grouped = defaultdict(list)
        for _, row in df.iterrows():
            grouped[row['Post Shortcode']].append(row['Comment'])

        # Get the 3 latest posts (assuming newest are at the top)
        latest_3_posts = list(grouped.keys())[:3]

        sentiment_results = {}
        for shortcode in latest_3_posts:
            comments = grouped[shortcode]
            if comments:
                scores = [TextBlob(comment).sentiment.polarity for comment in comments]
                average_score = sum(scores) / len(scores) if scores else 0
                sentiment_results[shortcode] = round(average_score, 3)
            else:
                sentiment_results[shortcode] = None  # no comments

        return jsonify(sentiment_results)

    except Exception as e:
        return jsonify({"error": str(e)})

# Add an API endpoint to fetch some data
@app.route('/api/data')
def get_data():
    # Sample data to return
    InfoDb = []
    InfoDb.append({
        "FirstName": "John",
        "LastName": "Mortensen",
        "DOB": "October 21",
        "Residence": "San Diego",
        "Email": "jmortensen@powayusd.com",
        "Owns_Cars": ["2015-Fusion", "2011-Ranger", "2003-Excursion", "1997-F350", "1969-Cadillac"]
    })
    InfoDb.append({
        "FirstName": "Shane",
        "LastName": "Lopez",
        "DOB": "February 27",
        "Residence": "San Diego",
        "Email": "slopez@powayusd.com",
        "Owns_Cars": ["2021-Insight"]
    })
    
    return jsonify(InfoDb)

# Add an HTML endpoint to say hello
@app.route('/')
def say_hello():
    html_content = """
    <html>
    <head>
        <title>Hellox</title>
    </head>
    <body>
        <h2>Hello, World!</h2>
    </body>
    </html>
    """
    return html_content

# Add an API endpoint to fetch an affirmation
@app.route('/api/affirmation')
def get_affirmation():
    affirmations = [
        "I am enough just as I am.",
        "I deserve love and respect.",
        "I choose to focus on my strengths.",
        "I am proud of the progress I’ve made.",
        "I trust myself to make the right decisions.",
        "I am capable of achieving great things.",
        "I radiate confidence and positivity.",
        "Challenges are opportunities for growth.",
        "I am in charge of my own destiny.",
        "My potential is limitless.",
        "I am strong and healthy.",
        "My body deserves care and nourishment.",
        "I honor my need for rest and rejuvenation.",
        "Every breath I take fills me with calm.",
        "I am grateful for my body and its abilities.",
        "I attract love and positivity.",
        "I communicate with honesty and kindness.",
        "I deserve meaningful connections.",
        "I am surrounded by supportive and loving people.",
        "I give and receive love freely."
    ]
    return jsonify(random.choice(affirmations))

# Load dataset and train model once
likes_data = pd.read_csv('datasets/legoland.csv')
X = likes_data[['Brightness', 'Saturation', 'Size']].values
y = likes_data['numLikes'].values

def average_likes():
    total_likes = likes_data["numLikes"].sum()
    num_posts = len(likes_data["numLikes"])
    return total_likes / num_posts

def classify_rating(score):
    if score >= 70:
        return "Excellent"
    elif score >= 50:
        return "Good"
    elif score >= 30:
        return "Moderate"
    else:
        return "Poor"

@app.route('/api/predict-likes', methods=['POST'])
def predict_likes():
    file = request.files.get('image')
    if not file:
        return jsonify({'error': 'No image uploaded'}), 400

    temp_path = 'temp_image.jpg'
    file.save(temp_path)

    try:
        brightness, saturation, size = extract_image_features(temp_path)
        X_new = np.array([[brightness, saturation, size]])
        prediction = model.predict(X_new)[0]

        avg_likes = average_likes()
        rating_score = 100 * prediction / avg_likes
        rating_label = classify_rating(rating_score)

        return jsonify({
            'brightness': brightness,
            'saturation': saturation,
            'size': size,
            'predicted_likes': prediction,
            'rating_score': rating_score,
            'rating_label': rating_label
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        os.remove(temp_path)


if __name__ == '__main__':
    # starts flask server on default port, http://127.0.0.1:5001
    app.run(port=5001)
