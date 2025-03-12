from sqlite3 import IntegrityError
from sqlalchemy import Text
from __init__ import app, db
from model.user import User
from model.group import Group
from datetime import datetime

class UserCars(db.Model):
    
    __tablename__ = 'userCars'
    id = db.Column(db.Integer, primary_key=True)
    _uid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    _make = db.Column(db.String(255), nullable=False) 
    _model = db.Column(db.String(255), nullable=False) 
    _year = db.Column(db.String(255), nullable=False) 
    _trim = db.Column(db.String(255), nullable=True) 
    _engine_type = db.Column(db.String(255), nullable=False) 
    _color = db.Column(db.String(255), nullable=True) 
    _vin = db.Column(db.String(255), nullable=True) 
    

    def __init__(self, uid, make, model, year, engine_type, trim="", color="", vin=""):
        # if make not in ['audi', 'apollo', 'bentley', 'bmw', 'bugatti', 'dodge', 'ferrari', 'ford', 'honda', 'hyundai', 'jaguar', 'kia', 'koenigsegg', 'lamborghini', 'lancia', 'mclaren', 'mercedes', 'nissan', 'pagani', 'porsche', 'ram', 'scion', 'tesla', 'toyota', 'volkswagen']:
        #     return {"message": "Bad Make!!"}, 404
        self._uid = uid
        self._make = make
        self._color = color
        self._engine_type = engine_type
        self._model = model
        self._year = year
        self._trim = trim
        self._vin = vin


    def __repr__(self):
        """
        The __repr__ method is a special method used to represent the object in a string format.
        Called by the repr(post) built-in function, where post is an instance of the Post class.
        
        Returns:
            str: A text representation of how to create the object.
        """
        return f"Post(id={self.id}, uid={self._uid}, make={self._make}, model={self._model}, trim={self._trim}, color={self._color}, engine_type={self._engine_type}, year={self._year}, vin={self._vin})"

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
            "uid": user.id if user else None,
            "make": self._make,
            "model": self._model,
            "year": self._year,
            "trim": self._trim,
            "color": self._color,
            "engine_type": self._engine_type,
            "vin": self._vin,
        }
        return data
    
    def update(self):
        """
        The update method commits the transaction to the database.
        
        Uses:
            The db ORM method to commit the transaction.
        
        Raises:
            Exception: An error occurred when updating the object in the database.
        """
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