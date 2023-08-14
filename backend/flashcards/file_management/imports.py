from backend import api, app, login_required
from flask_restful import Resource
from flask import jsonify, request, make_response
import TaskManager 
import os
import pandas as pd
from werkzeug.utils import secure_filename
import jwt
from backend.users import User
class imp(Resource): #/flashcards/import

    @login_required
    def post(self): 
        """
        Adds a new deck to the user with the listed cards front and back 
        Accepted file formats: *.csv, *.txt
            front, back
            something, somethignelse...
        The name of the csv will be taken as the name for the deck
        The key for the file SHOULD be 'file'
        Does this asynchronously
        """
        token = request.headers.get('token') 
        data = jwt.decode(token, app.config['SECRET_KEY'])
        user = User.query.filter_by(username = data['username']).first()

    
        f = request.files['file'] 
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], 'templates', str(user.id)))
        filename = secure_filename(f.filename)

        if not filename.split('.')[1] in ['csv', 'txt'] or not f: 
            return make_response(jsonify({"msg" : "File type is not correct"}))
        print('here')
        result = TaskManager.addCards.delay(filename, user.id)
        print(result.status)
        return make_response(jsonify({"msg" : "Processing file currently"}), 200 )
        

api.add_resource(imp, '/flashcards/import')