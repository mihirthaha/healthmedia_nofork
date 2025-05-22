from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from textblob import TextBlob
from collections import defaultdict
import random
import pandas as pd
import csv
import io
import pandas as pd
from sklearn.linear_model import LinearRegression
from PIL import Image, ImageStat
import numpy as np
import os
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

# Function for sentiment analysis from CSV content
def analyze_sentiment_from_csv(csv_content):
    sentiments = []
    
    try:
        # Use StringIO to read CSV content
        csv_file = io.StringIO(csv_content)
        reader = csv.DictReader(csv_file)
        
        # Check if required column exists
        if 'Comment' not in reader.fieldnames:
            return {"error": "CSV file must contain a 'Comment' column"}, 400
        
        for row_num, row in enumerate(reader, start=2):  # Start at 2 since row 1 is header
            comment = row['Comment'].strip() if row['Comment'] else ''
            
            if comment:  # Only analyze non-empty comments
                blob = TextBlob(comment)
                polarity = blob.sentiment.polarity
                subjectivity = blob.sentiment.subjectivity
                
                # Categorize sentiment
                if polarity > 0.1:
                    category = "positive"
                elif polarity < -0.1:
                    category = "negative"
                else:
                    category = "neutral"
                
                sentiment_data = {
                    "row_number": row_num,
                    "comment": comment,
                    "polarity": round(polarity, 3),
                    "subjectivity": round(subjectivity, 3),
                    "category": category
                }
                
                # Include additional data if available
                if 'Name' in row and row['Name']:
                    sentiment_data['name'] = row['Name']
                if 'ProfileUrl' in row and row['ProfileUrl']:
                    sentiment_data['profile_url'] = row['ProfileUrl']
                if 'Likes' in row and row['Likes']:
                    try:
                        sentiment_data['likes'] = int(row['Likes'])
                    except ValueError:
                        sentiment_data['likes'] = 0
                if 'Date' in row and row['Date']:
                    sentiment_data['date'] = row['Date']
                
                sentiments.append(sentiment_data)
        
        if not sentiments:
            return {"error": "No valid comments found in the CSV file"}, 400
        
        # Calculate summary statistics
        avg_polarity = sum(item['polarity'] for item in sentiments) / len(sentiments)
        avg_subjectivity = sum(item['subjectivity'] for item in sentiments) / len(sentiments)
        
        # Count sentiment categories
        positive_count = len([s for s in sentiments if s['category'] == 'positive'])
        neutral_count = len([s for s in sentiments if s['category'] == 'neutral'])
        negative_count = len([s for s in sentiments if s['category'] == 'negative'])
        
        total_comments = len(sentiments)
        
        return {
            "success": True,
            "summary": {
                "total_comments": total_comments,
                "average_polarity": round(avg_polarity, 3),
                "average_subjectivity": round(avg_subjectivity, 3),
                "sentiment_counts": {
                    "positive": positive_count,
                    "neutral": neutral_count,
                    "negative": negative_count
                },
                "sentiment_percentages": {
                    "positive": round((positive_count / total_comments) * 100, 1),
                    "neutral": round((neutral_count / total_comments) * 100, 1),
                    "negative": round((negative_count / total_comments) * 100, 1)
                }
            },
            "comments": sentiments
        }
    
    except Exception as e:
        return {"error": f"Error processing CSV: {str(e)}"}, 500

# Add an API endpoint for sentiment analysis (original)
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

# Add new API endpoint for CSV file upload and analysis
@app.route("/api/sentiment/upload", methods=["POST"])
def upload_and_analyze():
    """New endpoint for analyzing uploaded CSV files"""
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
        
        file = request.files['file']
        
        # Check if file was selected
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Check if file is CSV
        if not file.filename.lower().endswith('.csv'):
            return jsonify({"error": "File must be a CSV file"}), 400
        
        # Read file content
        try:
            csv_content = file.read().decode('utf-8')
        except UnicodeDecodeError:
            try:
                # Try with different encoding if UTF-8 fails
                file.seek(0)
                csv_content = file.read().decode('latin-1')
            except Exception as e:
                return jsonify({"error": "Unable to read file. Please ensure it's a valid CSV file."}), 400
        
        # Analyze sentiment
        result = analyze_sentiment_from_csv(csv_content)
        
        if isinstance(result, tuple):  # Error case
            return jsonify(result[0]), result[1]
        else:
            return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

# Add health check endpoint
@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "Sentiment analysis API is running"})

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
        "I am proud of the progress I've made.",
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