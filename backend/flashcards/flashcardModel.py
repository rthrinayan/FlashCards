from backend import db
import datetime
from sqlalchemy.sql import func 

class Deck(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50)) 
    colour = db.Column(db.String(50), default = "white")
    description = db.Column(db.String(300)) 
    score = db.Column(db.Integer, default = 0)
    created = db.Column(db.DateTime(timezone = True), default = datetime.datetime.now)
    last_seen = db.Column(db.DateTime(timezone = True), onupdate = func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    cards = db.relationship('Card', backref = 'deck', lazy = True) 

class Card(db.Model): 
    id = db.Column(db.Integer, primary_key = True)
    front = db.Column(db.String(200)) 
    back = db.Column(db.String(200)) 
    deck_id = db.Column(db.Integer, db.ForeignKey('deck.id'), nullable = False) #need to reference in lowercase
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)