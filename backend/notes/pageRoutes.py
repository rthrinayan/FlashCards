from flask import make_response, request
from backend.notes.noteModel import Notebook, Page
from backend import api, db, app, login_required
import jwt
import datetime
from flask_restful import Resource
from flask import jsonify, make_response
from backend.users import User

class allPages(Resource): 

    def get(self):
        """
        Returns all the page in the following format: 
            id 
            content
            notebook_id
            user_id"""
        
        pages = Page.query.all()
        output = []

        for page in pages: 
            pageObj = {
                'id' : page.id, 
                'content' : page.content, 
                'notbook_id' : page.notebook_id, 
                'user_id' : page.user_id
            }

            output.append(pageObj) 
        return make_response(jsonify(output), 200) 
    
    def post(self): 
        """Checks if current user is logged in and posts the page in his name
        Returns 201 if error as "error" : " <insert error here> " """
        token = request.headers.get('token') 
        data = jwt.decode(token, app.config['SECRET_KEY'])
        user = User.query.filter_by(username = data['username']).first()
        
        data = request.get_json()
        if not 'notebook_id' in data.keys(): 
            return make_response(jsonify({"error" : "Invalid attributes. Specify notebook id properly"}), 201) 

        notebook = Notebook.query.filter_by(id = data['notebook_id']).first()
        if not notebook: 
            return make_response(jsonify({'error' : 'Notebook does not exist'}), 201)

        notebook_id = notebook.id
        content = ''
        if 'content' in data.keys(): 
            content = data['content'] 
        user_id = user.id

        page = Page(content = content, notebook_id = notebook_id, user_id = user_id) 
        db.session.add(page) 
        db.session.commit() 
        page = Page.query.filter_by(content = content).first() 
        return make_response(jsonify({"id" : page.id}), 200) 

class singlePage(Resource): 
    @login_required 

    def get(self, pid): 
        """Returns specific page with id=pid in the format: 
            id
            content
            notebook_id 
            user_id
        """

        page = Page.query.filter_by(id = pid).first() 
        if not page : 
            return make_response(jsonify({'error' : 'Page does not exist'}), 201) 
            
        pageObj = {
            'id' : page.id, 
            'content' : page.content, 
            'notebook_id' : page.notebook_id, 
            'user_id' : page.user_id
        }

        return make_response(jsonify(pageObj),200) 

    def delete(self, pid): 
        """Deletes page with id = pid
        Checks if user is logged in"""

        token = request.headers.get('token') 
        data = jwt.decode(token, app.config['SECRET_KEY'])
        user = User.query.filter_by(username = data['username']).first()

        page = Page.query.filter_by(id = pid).first() 
        
        if  not page\
            or user.id != page.user_id: 
            return make_response(jsonify({'error' : 'You do not have permssion'}), 201) 
        
        Page.query.filter_by(id = pid).delete() 
        db.session.commit() 
        return 200

    
    def patch(self, pid): 
        """Checks intelligently for required information
        Updates last seen on notebook
        Checks if user is logged in
        200 - OK | 201 - error"""
        token = request.headers.get('token') 
        data = jwt.decode(token, app.config['SECRET_KEY'])
        user = User.query.filter_by(username = data['username']).first()

        data = request.get_json()   
        page = Page.query.filter_by(id = pid).first() 
        if user.id != page.user_id:
            return make_response(jsonify({'error' : 'You do not have permission'}), 201) 
        
        if 'content' in data.keys(): 
            page.content = data['content'] 
        
        Notebook.query.filter_by(id = page.notebook_id).first().last_seen = datetime.datetime.now() 
        db.session.commit() 
        return 200

class notebookPages(Resource):

    def get(self, nid):
        """Returns all the pages of the notebook with id = nid
        201 if notebook not found"""

        pages = Page.query.filter_by(notebook_id = nid) 

        if not pages: 
            return make_response(jsonify({'error' : 'Notebook has no pages'}), 201) 

        output =[]
        for page in pages: 
            pageObj = {
                'id' : page.id, 
                'content' : page.content, 
                'notebook_id' : page.notebook_id, 
                'user_id' : page.user_id
            }
            output.append(pageObj)
        
        return make_response(jsonify(output), 200) 

api.add_resource(allPages, '/page')
api.add_resource(singlePage, '/page/<int:pid>')
api.add_resource(notebookPages, '/notebook/pages/<int:nid>')


        
