import csv
import io
from flask import Flask, jsonify, request
from flask_cors import CORS
from textblob import TextBlob

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

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

def analyze_sentiment_from_file():
    """Original function for analyzing from existing file (kept for compatibility)"""
    sentiments = []
    COMMENTS_FILE = '/home/mihirthaha/nighthawk/healthmedia_backend-1/api/legoland_comments_all_posts.csv'
    
    try:
        with open(COMMENTS_FILE, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                comment = row['Comment'] 
                if comment.strip():  # Ignore empty comments
                    blob = TextBlob(comment)
                    sentiments.append({
                        "comment": comment,
                        "polarity": blob.sentiment.polarity,
                        "subjectivity": blob.sentiment.subjectivity
                    })

        if not sentiments:
            return {"error": "No valid comments found."}, 404

        avg_polarity = sum(item['polarity'] for item in sentiments) / len(sentiments)
        avg_subjectivity = sum(item['subjectivity'] for item in sentiments) / len(sentiments)

        return {
            "average_polarity": round(avg_polarity, 3),
            "average_subjectivity": round(avg_subjectivity, 3),
            "total_comments": len(sentiments),
            "comments": sentiments[:10]  # Return sample of 10
        }

    except Exception as e:
        return {"error": str(e)}, 500

@app.route("/api/sentiment", methods=["GET"])
def get_sentiment():
    """Original endpoint for analyzing existing file"""
    return jsonify(analyze_sentiment_from_file())

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

@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "Sentiment analysis API is running"})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
    
    # Instructions of Usage: 