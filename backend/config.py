import os

class DefaultConfig(object): 
    DEBUG = True 
    SQLALCHEMY_TRACK_MODIFICATIONS = False 
    SQLALCHEMY_DATABASE_URI = 'sqlite:///backend.db'
    SECRET_KEY = 'secret_key' 
    DEBUG = True 
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'backend/') 
    