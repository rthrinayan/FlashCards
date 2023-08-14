from backend import api, db, app, login_required
from backend.authentication.routes import login
from backend.quizzes.quizModel import Quiz, Question, Option 
from flask import jsonify, request, make_response
from flask_restful import Resource
import jwt 
from backend.users import User 

class allQuestions(Resource): 

    def get(self): 
        """Gets all the questions"""

        questions = Question.query.all() 
        output = []
        for ques in questions: 
            quesObj = {
                'id' : ques.id, 
                'content' : ques.content, 
                'user_id' : ques.user_id, 
                'quiz_id' : ques.quiz_id
            }

            output.append(quesObj) 
        return make_response(jsonify(output), 200) 
    
    def post(self) : 
        """Checks for attributes from request, all others set to default
        Returns 201 if user not logged in or quiz_id not given"""
        token = request.headers.get('token') 
        data = jwt.decode(token, app.config['SECRET_KEY'])
        user = User.query.filter_by(username = data['username']).first()

        data = request.get_json() 
        try: 
            quiz = Quiz.query.filter_by(id = data['quiz_id']).first() 

        except: 
            return make_response(jsonify({"error" : "Invalid attributes. Provide quiz id"}), 201) 


        content = '' 
        if 'content' in data.keys(): 
            content = data['content']
        marks = 1
        if 'marks' in data.keys(): 
            marks = data['marks']

        ques = Question(content = content, marks = marks, 
            quiz_id = data['quiz_id'], user_id = user.id)
        db.session.add(ques)
        
        db.session.commit() 
        return 200 

class singleQuestion(Resource): 
    @login_required
    def get(self, qid): 
        """ 
        Gets single question, login not required
        201 if doesn't exist"""
        
        ques = Question.query.filter_by(id = qid).first()  

        if not ques: 
            return make_response(jsonify({'error' : 'Does not exist'}), 201) 
        
        quesObj = {
                'id' : ques.id, 
                'content' : ques.content, 
                'user_id' : ques.user_id, 
                'quiz_id' : ques.quiz_id, 
                'marks' : ques.marks
            }
        return jsonify(quesObj) 
    
    def delete(self,qid): 
        """Checks for login
        If doesn't exist or not logged in 201
        Deletes it's options also
        """
        token = request.headers.get('token') 
        data = jwt.decode(token, app.config['SECRET_KEY'])
        user = User.query.filter_by(username = data['username']).first()

        ques = Question.query.filter_by(id = qid).first() 

        if not ques or\
            ques.user_id != user.id :
            return make_response(jsonify({'error' : 'Do not have permission'}), 201) 

        Option.query.filter_by(question_id = qid).delete()
        Question.query.filter_by(id = qid).delete()
        db.session.commit()
        return 200 

    def patch(self, qid): 
        """Updates only the given fields 
        201 if not logged in or no permission or quiz doesn't exist"""

        token = request.headers.get('token') 
        data = jwt.decode(token, app.config['SECRET_KEY'])
        user = User.query.filter_by(username = data['username']).first()  

        ques =Question.query.filter_by(id  = qid).first() 

        if not ques or\
            ques.user_id != user.id: 
            return make_response(jsonify({'error' : 'Do not have permission'}), 201) 
        
        data = request.get_json() 
        if 'content' in data.keys(): 
            ques.content = data['content']
        if 'marks' in data.keys(): 
            ques.marks = data['marks']
        
        db.session.commit() 
        return 200

class specificQuestion(Resource): 
    
    def get(self, qid): 
        questions = Question.query.filter_by(quiz_id = qid)
        output = [] 
        for ques in questions: 
            quesObj = {
                'id' : ques.id, 
                'content' : ques.content, 
                'user_id' : ques.user_id, 
                'quiz_id' : ques.quiz_id
            }
            output.append(quesObj ) 
        return make_response(jsonify(output), 200) 

    
api.add_resource(allQuestions, '/question')
api.add_resource(singleQuestion, '/question/<int:qid>')
api.add_resource(specificQuestion, '/quiz/questions/<int:qid>') 
