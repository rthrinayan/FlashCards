import datetime
import resource
from backend import app, login_required, api, db
from backend.flashcards import Card, Deck
from backend.users import User
from flask_restful import Resource
from flask import jsonify, request, make_response, request_tearing_down
import jwt

class allDecks(Resource):
    @login_required
    def get(self): 
        """
        Returns all the decks which have been made as iterable array
        The information is as follows:
            id
            name
            description 
            colour
            created 
            last_seen
            user_id"""

        decks = Deck.query.all() 
        output = []
        
        for deck in decks: 
            deckObj = {
                "id" : deck.id, 
                "name" : deck.name, 
                "description" : deck.description, 
                "colour" : deck.colour, 
                "created" : deck.created, 
                "last_seen" : deck.last_seen, 
                "user_id" : deck.user_id, 
                "score" : deck.score
            }

            output.append(deckObj) 
        
        return make_response(jsonify(output), 200)

    def post(self): 
        """
        Adds a deck with that particular id for that user
        Requires: 
            name, user_id 
        Can also take: 
            colour, description
        Returns 201 if data error or user not logged in"""
        
        token = request.headers.get('token') 
        data = jwt.decode(token, app.config['SECRET_KEY'])
        user = User.query.filter_by(username = data['username']).first()
        print(data)
        deck = request.get_json() 

        try: 
            colour = 'white'
            if 'colour' in deck.keys(): 
                colour = deck['colour']

            description = ''
            if 'description' in deck.keys(): 
                description = deck['description']

            created = datetime.datetime.now()

            last_seen = datetime.datetime.now()

            user_id = user.id 

            newDeck = Deck(
                name = deck['name'], 
                user_id = user_id, 
                colour = colour, 
                description = description, 
                created = created, 
                last_seen = last_seen, 
                score = 0
            )

            db.session.add(newDeck)
            db.session.commit() 
            return make_response(jsonify({"msg" : "Deck made", "did": newDeck.id, "uid" : newDeck.user_id}), 200 )
        
        except Exception as e: 
            print(e)
            return make_response(jsonify({"error" : "Invalid keys"}), 201)


class singleDeck(Resource):

    def get(self, did): 
        """
        Returns deck with that deck id
        If id doesn't exist returns 201 with error """

        deck = Deck.query.filter_by(id = did).first() 
        if not deck: 
            return make_response(jsonify({'error' : 'Deck with id {did} doesnt exist'}), 201) 

        deckObj = {
            "id" : deck.id, 
            "name" : deck.name, 
            "colour" : deck.colour, 
            "score" : deck.score, 
            "description" : deck.description, 
            "created" : deck.created, 
            "last_seen" : deck.last_seen, 
            "user_id" : deck.user_id
        }
        return jsonify(deckObj)

    def patch(self, did): 
        """
        Updates deck with did
        Checks for only the values that are udpated
        If user is not logged in returns 201"""

        oldDeck = Deck.query.filter_by(id = did).first()
        changes = request.get_json() 

        name = oldDeck.name
        colour = oldDeck.colour
        description = oldDeck.description
        last_seen = datetime.datetime.now()
        score = oldDeck.score

        if 'name' in changes.keys(): 
            name = changes['name']

        if 'colour' in changes.keys(): 
            colour = changes['colour'] 

        if 'description' in changes.keys(): 
            description = changes['description'] 
        
        if 'score' in changes.keys(): 
            score = changes['score']
        
        oldDeck.name = name
        oldDeck.colour = colour
        oldDeck.description = description
        oldDeck.last_seen = last_seen
        oldDeck.score = score
        db.session.commit() 
        return make_response(jsonify({"msg" : "Updated deck {did}"}), 200) 

    def delete(self, did):
        """
        Deletes Cards also
        Returns 201 if deck doesn't exist or user not logged in"""

        #checking if the deck exists at all
        if Deck.query.filter_by(id = did).first(): 
            Deck.query.filter_by(id = did).delete()
            Card.query.filter_by(deck_id = did).delete() 
            db.session.commit()

            return 200 

        else: 
            return make_response(jsonify({"error" : "Please log in"}), 201) 

class specificDecks(Resource): #user/deck

    def get(self): 
        """Returns all the decks of the current logged in user
        200 if ok 
        201 if error with error"""
        
        token = request.headers.get('token') 
        data = jwt.decode(token, app.config['SECRET_KEY'])     
        user = User.query.filter_by(username = data['username']).first()

        decks = Deck.query.filter_by(user_id = user.id)
        output = [] 
        
        for deck in decks: 
            deckObj = {} 

            deckObj = {
            "id" : deck.id, 
            "name" : deck.name, 
            "colour" : deck.colour, 
            "score" : deck.score, 
            "description" : deck.description, 
            "created" : deck.created, 
            "last_seen" : deck.last_seen, 
            "user_id" : deck.user_id
            }

            output.append(deckObj)

        return make_response(jsonify(output), 200)

api.add_resource(allDecks, '/deck') 
api.add_resource(singleDeck, '/deck/<int:did>')
api.add_resource(specificDecks, '/user/deck')
