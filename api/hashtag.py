from flask import Flask, request, jsonify
from model import db, Hashtag
import csv

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hashtags.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/add_hashtag', methods=['POST'])
def add_hashtag():
    data = request.get_json()
    tag = Hashtag.query.filter_by(hashtag=data['hashtag']).first()
    
    if tag:
        tag.total_posts += 1
        tag.average_likes = (tag.average_likes * (tag.total_posts - 1) + data['likes']) / tag.total_posts
        tag.average_comments = (tag.average_comments * (tag.total_posts - 1) + data['comments']) / tag.total_posts
        tag.average_reach = (tag.average_reach * (tag.total_posts - 1) + data['reach']) / tag.total_posts
    else:
        tag = Hashtag(
            hashtag=data['hashtag'],
            total_posts=1,
            average_likes=data['likes'],
            average_comments=data['comments'],
            average_reach=data['reach']
        )
        db.session.add(tag)

    db.session.commit()
    return jsonify({"message": "Hashtag data updated!"}), 200

@app.route('/get_effectiveness', methods=['GET'])
def get_effectiveness():
    hashtags = Hashtag.query.all()
    sorted_hashtags = sorted(hashtags, key=lambda x: x.calculate_effectiveness(), reverse=True)

    return jsonify([{
        "hashtag": h.hashtag,
        "effectiveness": h.calculate_effectiveness(),
        "total_posts": h.total_posts,
        "average_likes": h.average_likes,
        "average_comments": h.average_comments,
        "average_reach": h.average_reach
    } for h in sorted_hashtags]), 200

# 🔗 New endpoint for your frontend
@app.route('/api/hashtag-analysis', methods=['POST'])
def analyze_hashtags():
    data = request.get_json()
    hashtags = [tag.strip().lower() for tag in data['hashtags'].split()]
    avg_total = 0
    count = 0

    for tag in hashtags:
        tag = tag.lstrip('#')  # remove the '#' character
        h = Hashtag.query.filter_by(hashtag=tag).first()
        if h:
            avg_total += h.average_likes
            count += 1

    if count == 0:
        return jsonify({"views": 0})

    average = avg_total / count
    return jsonify({"views": round(average)})

# 🔄 Optional CSV loader
@app.route('/load_csv', methods=['POST'])
def load_csv():
    file_path = request.json.get("file_path")
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            tag = row['hashtag']
            likes = float(row['likes'])
            comments = float(row.get('comments', 0))
            reach = float(row.get('reach', 0))

            existing = Hashtag.query.filter_by(hashtag=tag).first()
            if existing:
                existing.total_posts += 1
                existing.average_likes = (existing.average_likes * (existing.total_posts - 1) + likes) / existing.total_posts
                existing.average_comments = (existing.average_comments * (existing.total_posts - 1) + comments) / existing.total_posts
                existing.average_reach = (existing.average_reach * (existing.total_posts - 1) + reach) / existing.total_posts
            else:
                new_tag = Hashtag(
                    hashtag=tag,
                    total_posts=1,
                    average_likes=likes,
                    average_comments=comments,
                    average_reach=reach
                )
                db.session.add(new_tag)
        db.session.commit()
    return jsonify({"message": "CSV loaded!"})
