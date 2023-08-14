import datetime
from backend import api, db, app, login_required
import jwt
from backend.authentication.routes import login
from backend.quizzes.quizModel import Quiz, Question, Option 
from flask import jsonify, request, make_response
from flask_restful import Resource
from backend.users import User
class allQuizzes(Resource): 

    def get(self): 
        """
        Returns all the Quizzes in iterable array
        """

        output = []
        quizzes = Quiz.query.all() 

        for quiz in quizzes: 
            quizObj = {
                'id' : quiz.id, 
                'name' : quiz.name, 
                'colour' : quiz.colour, 
                'description' : quiz.description, 
                'score' : quiz.score, 
                'created' : quiz.created, 
                'duration' : quiz.duration, 
                'user_id' : quiz.user_id
            }

            output.append(quizObj) 
        return make_response(jsonify(output), 200) 

    def post(self): 
        """"
        Only sets the given attributes. Rest all are set to the default
        201 if name not given or not logged in """
        token = request.headers.get('token') 
        data = jwt.decode(token, app.config['SECRET_KEY'])
        user = User.query.filter_by(username = data['username']).first()

        data = request.get_json()
        try : 
            name = data['name'] 
        except: 
            return make_response(jsonify({"error" : "Invalid keys"}), 201) 
        
        colour = 'white' 
        if 'colour' in data.keys(): 
            colour = data['colour']
        
        description = '' 
        if 'description' in data.keys(): 
            description = data['description'] 
        
        score = 0 

        created = datetime.datetime.now() 

        duration = 20 
        if 'duration' in data.keys(): 
            duration = data['duration'] 
        
        user_id = user.id

        quiz = Quiz(name = name, colour = colour, description = description,
            score = score, created = created, duration = duration, user_id = user_id) 
        
        db.session.add(quiz) 
        db.session.commit()
        return 200 

class singleQuiz(Resource): 
    @login_required
    def get(self, qid): 
        """
        Gets the specific quiz with all attributes
        201 if quiz does't exist
        Don't need to be logged in """

        quiz = Quiz.query.filter_by(id = qid).first() 
        if not quiz: 
            return make_response(jsonify({"error" : "quiz doesn't exist"}), 201) 
        
        quizObj = {
            'id' : quiz.id,
            'name' : quiz.name, 
            'colour' : quiz.colour, 
            'description' : quiz.description, 
            'score' : quiz.score,
            'created' : quiz.created, 
            'duration' : quiz.duration, 
            'user_id' : quiz.user_id 
        }

        return make_response(jsonify(quizObj), 200) 
    
    def delete(self, qid): 
        """
        Deletes quiz and all questions and options for questions
        Checks for login 
        201 if quiz doesn't exist or not logged in """
        token = request.headers.get('token') 
        data = jwt.decode(token, app.config['SECRET_KEY'])
        user = User.query.filter_by(username = data['username']).first()

        quiz = Quiz.query.filter_by(id = qid).first()

        if not quiz or\
            quiz.user_id != user.id :
            return make_response(jsonify({'error' : 'Do not have permission'}), 201) 

        Option.query.filter_by(quiz_id = quiz.id).delete() 
        Question.query.filter_by(quiz_id = quiz.id).delete() 
        Quiz.query.filter_by(id = qid).delete() 

        db.session.commit() 
        return 200

    def patch(self, qid) : 
        """
        Only updates paramters which have been given 
        Checks if logged in 
        Returns 201 incase no quiz or not logged in """

        quiz = Quiz.query.filter_by(id = qid).first() 
        token = request.headers.get('token') 
        data = jwt.decode(token, app.config['SECRET_KEY'])
        user = User.query.filter_by(username = data['username']).first()

        if not quiz or\
            quiz.user_id != user.id:
            return make_response(jsonify({'error' : 'Do not have permission'}), 201) 
        
        data = request.get_json() 
        if 'name' in data.keys(): 
            quiz.name = data['name']
        if 'colour' in data.keys(): 
            quiz.colour = data['colour']
        if 'description' in data.keys(): 
            quiz.description = data['description']
        if 'score' in data.keys(): 
            quiz.score = data['score']
        if 'duration' in data.keys():
            quiz.duration = data['duration']  
            
        db.session.commit() 
        return 200 

class specificQuiz(Resource): 
    @login_required

    def get(self):
        """Gets all quizzes for logged in user"""
        token = request.headers.get('token') 
        data = jwt.decode(token, app.config['SECRET_KEY'])
        user = User.query.filter_by(username = data.username).first()
        quizzes = Quiz.query.filter_by(user_id = user.id).first()
        output = []
        for quiz in quizzes: 

            quizObj = {
                'id' : quiz.id,
                'name' : quiz.name, 
                'colour' : quiz.colour, 
                'description' : quiz.description, 
                'score' : quiz.score,
                'created' : quiz.created, 
                'duration' : quiz.duration, 
                'user_id' : quiz.user_id 
            }

            output.append(quizObj) 
        return make_response(jsonify(output), 200) 

api.add_resource(allQuizzes, '/quiz') 
api.add_resource(singleQuiz, '/quiz/<int:qid>') 
api.add_resource(specificQuiz, '/user/quizzes') 
