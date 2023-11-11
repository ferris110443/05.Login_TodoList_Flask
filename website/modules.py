from flask import Flask
from sqlalchemy import Integer, String , DateTime , func,Column,ForeignKey
from flask_login import UserMixin
from . import db

class User(db.Model,UserMixin):
    id = Column(Integer, primary_key=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    email = Column(String(255), unique=True)
    password = Column(String(255))
    notes = db.relationship('Note')

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password


class Note(db.Model):
    id = Column(Integer,primary_key=True)
    data = Column(String(1000))
    date = Column(DateTime(timezone=True),default=func.now())
    user_id = Column(Integer,ForeignKey('user.id'))
    