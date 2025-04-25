import requests
from sqlite3 import IntegrityError
from sqlalchemy import Text
from __init__ import app, db
from model.user import User
from model.group import Group

class Statistics(db.Model):
    """
    Statistics Model
    The Statistics class represents the stats for posts with likes, views, and time.
    """
    __tablename__ = 'timeofday'
    id = db.Column(db.Integer, primary_key=True)
    likes = db.Column(db.Integer, nullable=False, unique=False)
    time = db.Column(db.Integer, unique=False, nullable=False)

    def __init__(self, likes, views, time):
        self.likes = likes
        self.time = time

    def create(self):
        """
        Adds the object to the database and commits the transaction.
        """
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def read(self):
        """
        Returns the object data as a dictionary.
        """
        return {
            "id": self.id,
            "likes": self.likes,
            "time": self.time
        }

    def update(self):
        """
        Updates the object in the database.
        """
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def delete(self):
        """
        Deletes the object from the database.
        """
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def restore(data):
        for sbuser_data in data:
            _ = sbuser_data.pop('id', None)
            sbuser = Statistics.query.filter_by(likes=sbuser_data.get("likes")).first()
            if sbuser:
                sbuser.update(sbuser_data)
            else:
                sbuser = Statistics(**sbuser_data)
                sbuser.create()

def fetch_and_insert_posts():
    """
    Fetches the posts from the API and inserts them into the Statistics table.
    """
    url = "http://localhost:8887/api/posts"
    response = requests.get(url)

    if response.status_code == 200:
        posts = response.json().get("posts", [])

        for post in posts:
            likes_views = post.get("likes_views", 0)
            time_of_day = post.get("time_of_day", 0)

            # Insert each post into the database
            stat = Statistics(likes=likes_views, likes=likes_views, time=time_of_day)
            try:
                stat.create()  # Insert into the database
                print(f"Record created: {stat.read()}")
            except IntegrityError:
                db.session.rollback()  # In case of duplicate or error
                print(f"Error with post: {post['url']}")
    else:
        print(f"Failed to fetch posts from API. Status code: {response.status_code}")

def initstats():
    """
    Initializes the database by creating the Statistics table and populating it with data.
    """
    with app.app_context():
        """Create database and tables"""
        db.create_all()

        # Fetch and insert posts into the database
        fetch_and_insert_posts()

if __name__ == "__main__":
    initstats()
