from backend import app, login_required, api, db 
from backend.users.userModel import User
from flask_restful import Resource
from flask import jsonify, request, make_response
import jwt

class allUsers(Resource): 
    
    def get(self): 
        """
        Returns all the users in the database as an iterable array
        The elements in the array are users with data members: 
            id
            username
            repuation 
            email 
        """
        users = User.query.all()
        output = []

        for user in users: 
            userObj = {} 
            userObj['id'] = user.id
            userObj['username'] = user.username
            userObj['reputation'] = user.reputation
            userObj['email'] = user.email
            output.append(userObj)
        return jsonify(output) 
    
    def post(self): 
        """
        Adds a new user to the database after verifying the information
        Username and email must not collide returns resopnse 201 
        Password must be greater than 8 characters
        Body must have the following: 
            username, email, password, phone_number (optional) 
        Returns error if any
        """
        data = request.get_json()
        #check if matching usernames, email
        users = User.query.filter((User.username == data['username']) | (User.email == data['email'])).first()   
        if users: 
            error = 'User already exists' 
            return make_response(jsonify({'error' : error }), 201)
        phone_number = '0000000000'
        if 'phone_number' in data.keys(): 
            phone_number = data['phone_number']
        try:    
            user = User(username = data['username'], 
                password = data['password'], 
                reputation = 0, 
                email = data['email'], 
                phone_number = phone_number
            ) 
            db.session.add(user) 
            db.session.commit() 
            return 200
        except TypeError: 
            error = 'You have not provided all the information' 
            return make_response(jsonify({"error" : error}), 201) 

class singleUser(Resource): 
    @login_required
    def get(self, uid): 
        """
        Searches the database for a user with id == uid and returns: 
            username
            email
            phone number 
            reputation
        Returns 201 if not found
        """

        user = User.query.filter_by(id = uid).first() 
        
        if not user: 
            return make_response(jsonify({'error' : 'User does not exit'}), 201) 

        filteredUser = {
            'id': user.id, 
            'username' : user.username,
            'email' : user.email, 
            'phone_number' : user.phone_number, 
            'reputation' : user.reputation,
        }

        return make_response(jsonify(filteredUser), 200)

    def patch(self, uid): 
        """
        Updates the user details other than email
        Checks for username clash, return 202 if clash 
        All data not provided is autofilled
        If user with uid not found returns 201
        If user not logged in, returns 203"""
        token = request.headers.get('token') 
        data = jwt.decode(token, app.config['SECRET_KEY'])
        user = User.query.filter_by(username = data.username).first()

        if not user.id == uid:
            return make_response(jsonify({'error' : 'Please log in '}), 203) 


        user = User.query.filter_by(id = uid).first() 

        if not user: 
            return make_response(jsonify({"error" : "User doesn't exist"}), 201)
        
        data = request.get_json() 
        if data['username']:
            clashUser = User.query.filter_by(username = data['username']).first() 
            if clashUser:
                return make_response(jsonify({"error" : "Username already exists"}), 202)
        
            user.username = data['username'] 
        
        if data['phone_number']:
            user.phone_number = data['phone_number'] 

        db.session.commit()         
        return 200 

    def delete(self, uid): 
        """
        Deletes user with uid 
        If user doesn't exist returns 201
        If user not logged in returns 202
        """

        if not user.id == uid:
            return make_response(jsonify({'error' : 'Please log in '}), 202) 


        user = User.query.filter_by(id = uid) 
        if not user: 
            return make_response(jsonify({"error" : "User doesn't exist"}), 201) 
        
        User.query.filter_by(id = uid).delete()
        db.session.commit() 

        return 200 


api.add_resource(allUsers, '/user')
api.add_resource(singleUser, '/user/<int:uid>')