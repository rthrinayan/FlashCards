from backend import db, api 
import datetime

class Quiz(db.Model): 
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50)) 
    colour = db.Column(db.String(50), default = "white") 
    description = db.Column(db.String(100))
    score = db.Column(db.Integer, default = 0) 
    created = db.Column(db.DateTime(timezone = True), default = datetime.datetime.now())
    duration = db.Column(db.Integer, default = 20) #units are minutes. Don't need more precision 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    question = db.relationship('Question', backref = 'quiz', lazy = True) 
    option = db.relationship('Option', backref = 'quiz', lazy = True) 

class Question(db.Model): 
    id = db.Column(db.Integer, primary_key = True) 
    content = db.Column(db.String(100)) 
    marks = db.Column(db.Integer, default = 0) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False) 
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable = False) 

    option = db.relationship('Option', backref = 'question', lazy = True)
    
class Option(db.Model): 
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(50)) 
    correct = db.Column(db.Boolean, default = False) 
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable = False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable = False) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False) 


