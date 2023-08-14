from backend import api, db, app, login_required
from backend.authentication.routes import login
from backend.quizzes.quizModel import Quiz, Question, Option 
from flask import jsonify, request, make_response
from flask_restful import Resource
import jwt 
from backend.users import User

class allOptions(Resource): 

    def get(self): 

        token = request.headers.get('token') 
        data = jwt.decode(token, app.config['SECRET_KEY'])
        user = User.query.filter_by(username = data['username']).first()
    
        opts = Option.query.all()
        output = []
        for opt in opts: 
            optObj = {
                'id' : opt.id,
                'content' : opt.content, 
                'correct' : opt.correct, 
                'question_id' : opt.question_id, 
                'quiz_id' : opt.quiz_id, 
                'user_id' : opt.user_id
            }
            output.append(optObj)
        return make_response(jsonify(output), 200) 

    def post(self): 
        token = request.headers.get('token') 
        data = jwt.decode(token, app.config['SECRET_KEY'])
        user = User.query.filter_by(username = data['username']).first()

        data = request.get_json() 
        try: 
            question  =Question.query.filter_by(id = data['question_id']).first() 

        except Exception as e : 
            print(e)
            return make_response(jsonify({'error' : f'invalid arguments, provide question id'}), 201)


        content = ''
        if 'content' in data.keys(): 
            content = data['content'] 
        
        corrent = False 
        if 'correct' in data.keys(): 
            correct = False if (data['correct'].lower() == "false" ) else 1 
        
        question_id = data['question_id'] 

        quiz_id = question.quiz.id

        user_id = user.id 

        opt = Option(content = content, correct = correct, 
            question_id = question_id, quiz_id = quiz_id, user_id = user_id )
        
        db.session.add(opt) 

        db.session.commit() 

        return 200

class singleOption(Resource): 
    @login_required
    
    def get(self, oid): 

        opt = Option.query.filter_by(id = oid).first()

        if not opt: 
            return make_response(jsonify({'error' : "Option doesn't exist"}),201)
        
        optObj = {
            'id' : opt.id,
            'content' : opt.content, 
            'correct' : opt.correct, 
            'question_id' : opt.question_id, 
            'quiz_id' : opt.quiz_id, 
            'user_id' : opt.user_id
        }

        return make_response(jsonify(optObj), 200) 
    
    def patch(self, oid): 

        opt = Option.query.filter_by(id = oid).first() 

        data = request.get_json() 

        if 'content' in data.keys():
            opt.content = data['content']
        if 'correct' in data.keys(): 
            value = data['correct'] 
            opt.correct = 0 if data['correct'] == 'false' else 1 

        db.session.commit() 

        return 200 

    def delete(self, oid): 

        token = request.headers.get('token') 
        data = jwt.decode(token, app.config['SECRET_KEY'])
        user = User.query.filter_by(username = data['username']).first()

        opt = Option.query.filter_by(id = oid).first()  
        if user.id == opt.id: 
            Option.query.filter_by(id = oid).delete( )
            db.session.commit() 
            return 200 
        else: 
            return make_response(jsonify({'error' : "Don't have permission"}), 201) 

class specificOption(Resource): 

    def get(self, qid): 
        
        opts = Option.query.filter_by(question_id = qid) 
        output = []
        for opt in opts: 
            optObj = {
                'id' : opt.id,
                'content' : opt.content, 
                'correct' : opt.correct, 
                'question_id' : opt.question_id, 
                'quiz_id' : opt.quiz_id, 
                'user_id' : opt.user_id
            }
            output.append(optObj)
        return make_response(jsonify(output), 200) 

api.add_resource(allOptions, '/option')
api.add_resource(singleOption, '/option/<int:oid>') 
api.add_resource(specificOption, '/question/option/<int:qid>')