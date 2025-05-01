from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import random
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
        with open("/home/mihirthaha/nighthawk/healthmedia_backend-1/api/legoland_comments_all_posts.csv", newline='', encoding='utf-8') as csvfile:
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
def get_sentiment():
    comments = get_comments_from_file()  # Get comments from the CSV file
    
    if not comments:
        return jsonify({"error": "No comments available to analyze."}), 400  # Handle the case where no comments are found
    
    total_sentiment_score = 0
    for comment in comments:
        sentiment = analyze_sentiment(comment)  # Perform sentiment analysis
        total_sentiment_score += sentiment

    # Calculate the average sentiment score if there are comments
    if len(comments) > 0:
        average_sentiment = total_sentiment_score / len(comments)
    else:
        average_sentiment = 0  # If no comments, set to 0

    return jsonify({"average_sentiment": average_sentiment})

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
    if score >= 90:
        return "Excellent"
    elif score >= 75:
        return "Good"
    elif score >= 60:
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
        rating_score = 75 * prediction / avg_likes
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
