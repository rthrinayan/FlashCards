from flask import Flask, session, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api 
from flask_cors import CORS
from functools import wraps
import jwt

app = Flask(__name__, instance_relative_config = True) 
app.config.from_object('backend.config.DefaultConfig')
app.secret_key = 'secret_key' #secret key for sessions
CORS(
    app, 
    supports_credentials=True
    ) #to make requests from frontend

api = Api(app) 

db = SQLAlchemy(app) 

#used to return information from user object later on in the app
#Will use the userobject.property to verify login later on 
def login_required(f): 
    @wraps(f)
    def decorated(*args, **kwargs): 
        token = request.headers.get('token') 

        try : 
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except: 
            return jsonify({'msg' : 'Token is missing'})
        return f(*args, **kwargs) 
    return decorated 
    
#importing api routes | not necessary, jic
from backend.flashcards import deckRoutes, cardRoutes, file_management
from backend.users import userRoutes
from backend.authentication import routes
from backend.notes import pageRoutes, notebookRoutes
from backend.quizzes import questionRoutes, optionRoutes, quizRoutes

#importing models
from backend.flashcards import Deck, Card
from backend.users.userModel import User
from backend.notes import Notebook, Page
from backend.quizzes import Quiz, Question, Option