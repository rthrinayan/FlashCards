from enum import unique
from flask_login import UserMixin
from backend import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True) 
    username = db.Column(db.String(50), unique = True) 
    email = db.Column(db.String(100), unique = True)
    password = db.Column(db.String(20), unique = False) 
    phone_number = db.Column(db.String(10), default = '0000000000') 
    reputation = db.Column(db.Integer(), default = 0)

    decks = db.relationship('Deck', backref = 'user', lazy = True) 
    cards = db.relationship('Card', backref = 'user', lazy = True) 
    notebook = db.relationship('Notebook', backref = 'user', lazy = True) 
    page = db.relationship('Page', backref = 'user', lazy = True )
    quiz = db.relationship('Quiz', backref = 'user', lazy = True) 
    question = db.relationship('Question', backref = 'user', lazy = True) 
    option = db.relationship('Option', backref = 'user', lazy = True) 
    