from sqlite3 import IntegrityError
from sqlalchemy import Text
from __init__ import app, db
from datetime import datetime



class MechanicsTip(db.Model):
    """
    MechanicsTip Model
    Represents a table of tips with corresponding make, model, year, and issue.
    """
    __tablename__ = 'mechanicsTips'
    id = db.Column(db.Integer, primary_key=True)
    _make = db.Column(db.String(255), nullable=False)
    _model = db.Column(db.String(255), nullable=False)
    _year = db.Column(db.String(255), nullable=False)
    _issue = db.Column(db.String(255), nullable=False)
    _tip = db.Column(db.String(1024), nullable=True)
    _date_added = db.Column(db.DateTime, default=datetime.now)


    def __init__(self, uid, make, model, year, issue, tip):
        print(uid)
        self._make = make
        self._model = model
        self._year = year
        self._issue = issue
        self._tip = tip

    def __repr__(self):
        return f"MechanicsTip(id={self.id}, make={self._make}, model={self._model}, year={self._year}, issue={self._issue}, tip={self._tip})"

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            raise error

    def read(self):
        return {
            "id": self.id,
            "make": self._make,
            "model": self._model,
            "year": self._year,
            "issue": self._issue,
            "tip": self._tip,
            "date_added": self._date_added
        }

    def update(self):
        try:
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            raise error

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            raise error

