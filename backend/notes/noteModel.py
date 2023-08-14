from sqlalchemy.sql import func
from backend import db
import datetime 

class Notebook(db.Model): 
    id = db.Column(db.Integer, primary_key = True) 
    name = db.Column(db.String(50)) 
    colour = db.Column(db.String(50)) 
    description = db.Column(db.String(200)) 
    created  = db.Column(db.DateTime(timezone = True), default = datetime.datetime.now()) 
    last_seen = db.Column(db.DateTime(timezone = True), default = func.now()) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = True) 

    pages = db.relationship('Page', backref = 'notebook', lazy = True)

class Page(db.Model): 
    id = db.Column(db.Integer, primary_key = True) 
    content = db.Column(db.String(1000)) 
    notebook_id = db.Column(db.Integer, db.ForeignKey('notebook.id'), nullable = False) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)