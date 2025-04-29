from flask import Flask, request, jsonify
from model import db, hashtag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hashtags.db'
db.init_app(app)

@app.route('/add_hashtag', methods=['POST'])
def add_hashtag():
    data = request.get_json()
    hashtag = Hashtag.query.filter_by(hashtag=data['hashtag']).first()
    
    if hashtag:
        hashtag.total_posts += 1
        hashtag.average_likes = (hashtag.average_likes * (hashtag.total_posts - 1) + data['likes']) / hashtag.total_posts
        hashtag.average_comments = (hashtag.average_comments * (hashtag.total_posts - 1) + data['comments']) / hashtag.total_posts
        hashtag.average_reach = (hashtag.average_reach * (hashtag.total_posts - 1) + data['reach']) / hashtag.total_posts
    else:
        hashtag = Hashtag(hashtag=data['hashtag'], total_posts=1, average_likes=data['likes'], 
                          average_comments=data['comments'], average_reach=data['reach'])
        db.session.add(hashtag)

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

if __name__ == '__main__':
    app.run(debug=True)
