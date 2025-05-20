import csv
from flask import Flask, jsonify
from textblob import TextBlob

app = Flask(__name__)

COMMENTS_FILE = '/home/mihirthaha/nighthawk/healthmedia_backend-1/api/legoland_comments_all_posts.csv'

def analyze_sentiment():
    sentiments = []

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
    return jsonify(analyze_sentiment())

if __name__ == "__main__":
    app.run(debug=True)
