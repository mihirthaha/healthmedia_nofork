from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Hashtag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hashtag = db.Column(db.String(100), unique=True, nullable=False)
    total_posts = db.Column(db.Integer, default=0)
    average_likes = db.Column(db.Float, default=0.0)
    average_comments = db.Column(db.Float, default=0.0)
    average_reach = db.Column(db.Float, default=0.0)  # Reach or Impressions data

    def __repr__(self):
        return f'<Hashtag {self.hashtag}>'

    def calculate_effectiveness(self):
        # Example metric: Average of likes, comments, and reach
        return (self.average_likes + self.average_comments + self.average_reach) / 3
