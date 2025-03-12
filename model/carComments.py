from sqlite3 import IntegrityError
from sqlalchemy import Text
from __init__ import app, db
from datetime import datetime
from model.user import User

class CarComments(db.Model):

    __tablename__ = "carcomments" 
    id = db.Column(db.Integer, primary_key=True)
    _uid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    _post_id = db.Column(db.Integer, db.ForeignKey("carPosts.id"), nullable=False)
    _content = db.Column(db.String(255), nullable=False)
    _date_posted = db.Column(db.DateTime, nullable=False)


    def __init__(self, uid, post_id, content, date_posted=None):
        self._uid = uid 
        self._post_id = post_id
        self._content = content
        self._date_posted = datetime.fromisoformat(date_posted) if date_posted else datetime.now()

    def __repr__(self):
        """
        The __repr__ method is a special method used to represent the object in a string format.
        Called by the repr(post) built-in function, where post is an instance of the Post class.
        
        Returns:
            str: A text representation of how to create the object.
        """
        return f"CarComment(id={self.id}, uid={self._uid}, post_id={self._post_id}, content={self._content}, date_posted={self._date_posted})"
        
    def create(self):
        """
        The create method adds the object to the database and commits the transaction.
        
        Uses:
            The db ORM methods to add and commit the transaction.
        
        Raises:
            Exception: An error occurred when adding the object to the database.
        """
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            raise error
        
    def read(self):
        """
        The read method retrieves the object data from the object's attributes and returns it as a dictionary.
        
        Uses:
            The Group.query and User.query methods to retrieve the group and user objects.
        
        Returns:
            dict: A dictionary containing the post data, including user and group names.
        """
        user = User.query.get(self._uid)
        data = {
            "id": self.id,
            "content": self._content,
            "user": {
                "name": user.read()["name"],
                "id": user.read()["id"],
                "uid": user.read()["uid"],
                "email": user.read()["email"],
                "pfp": user.read()["pfp"]
            },
            "postid": self._post_id,
            "date_posted": self._date_posted
        }
        return data
    
    def update(self, data=None):
        
        """
        The update method commits the transaction to the database.
        
        Uses:
            The db ORM method to commit the transaction.
        
        Raises:
            Exception: An error occurred when updating the object in the database.
        """

        if data:
            self._content = data.get("content", self._content)
            self._uid = data.get("uid", self._uid)
            self._date_posted = datetime.fromisoformat(data.get("date_posted", self._date_posted))
            self._post_id = data.get("postid", self._post_id)
        try:
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            raise error
        
    def delete(self):
        """
        The delete method removes the object from the database and commits the transaction.
        
        Uses:
            The db ORM methods to delete and commit the transaction.
        
        Raises:
            Exception: An error occurred when deleting the object from the database.
        """    
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            raise error
        
    @staticmethod
    def restore(data):
        users = {}
        for carComment_data in data:
            id = carComment_data.get("id")
            comment = CarComments.query.filter_by(id=id).first()
            if comment:
                comment.update(carComment_data)
            else:
                comment = CarComments(carComment_data.get("uid"), carComment_data.get("postid"), carComment_data.get("content"), carComment_data.get("date_posted"))
                comment.create()
        return users