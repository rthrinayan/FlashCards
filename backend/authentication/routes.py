from backend import api, app, login_required
from backend.users.userModel import User 
from flask import jsonify, request, make_response
from flask_restful import Resource
import jwt
import datetime

class login(Resource): 

    def get(self): 
        """
        Takes in the email, username and password information as the authentication in the header of request
        Returns the token in the body of the message
        If username doesn't exist or password doesn't match returns 404
        200 if success
        """
        auth = request.authorization
        print(auth) 
        
        user = User.query.filter_by(username = auth.username).first() 
        userObj = {
            'id': user.id, 
            'username' : user.username, 
            'phone_number' : user.phone_number, 
            'email' : user.email
        }
        if auth and user and user.password ==  auth.password: #if the user exists and password matches
            token = jwt.encode({'username' : auth.username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
            return jsonify({'token' : token.decode('UTF-8'), 'usr' : userObj})
        else:   
            return make_response('could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})

class logout(Resource):
    """
    Sending a get or a post request logs out the current user
    """
    @login_required
    def get(self): 

        return make_response(jsonify({"msg": "Logout succesfull"}), 200)
    
    def post(self): 
        
        return make_response(jsonify({"msg": "Logout succesfull"}), 200)


api.add_resource(login, '/login')
api.add_resource(logout, '/logout') 
