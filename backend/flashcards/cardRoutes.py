import datetime
from backend import app, api, db, login_required 
from backend.flashcards import Card, Deck
from backend.users import User
from flask_restful import Resource
from flask import jsonify, request, make_response
import jwt

class allCards(Resource):
    @login_required
    def get(self):
        """
        Returns all the cards as an iterable array"""

        output = [] 
        cards = Card.query.all()
        
        for card in cards: 
            cardObj = {}
            cardObj = {
                "id" : card.id, 
                "front" : card.front, 
                "back" : card.back, 
                "deck_id" : card.deck_id, 
                "user_id" : card.user_id
            }
            print(cardObj['front'], cardObj['back'])
            output.append(cardObj)
        
        return make_response(jsonify(output), 200)

    def post(self): 
        """
        Selectively fills the data and creates a card for the logged in user
        Data must contain: 
            front, back, deck_id
        returns 201 if invalid keys or log in issue"""
        
        card = request.get_json()

        try: 
            token = request.headers.get('token') 
            data = jwt.decode(token, app.config['SECRET_KEY'])
            username = data['username']

            front = card['front']
            back = card['back']
            deck_id = card['deck_id']
            
            #checks if the deck belongs to the current logged in user
            deck = Deck.query.filter_by(id = deck_id).first()
            user = User.query.filter_by(username = username).first() 
            if deck.user_id == user.id:
                deck = Card(front = front,
                    back = back, 
                    deck_id = deck_id, 
                    user_id = user.id)
                db.session.add(deck)
                db.session.commit() 

                return make_response(jsonify({"msg" : "created card", "cid" : deck.id, "did" : deck.deck_id, "uid" : deck.user_id}), 200)

            else: 
                return make_response(jsonify({"error" : "Please log in"}), 201)
        except Exception as e: 
            print(e)
            return make_response(jsonify({"error" : "invalid keys"}), 201)


class singleCard(Resource): 
    @login_required
    def get(self, cid): 
        """ 
        Gets that specific card, no need for login
        If card doesn't exit return 201"""

        card = Card.query.filter_by(id = cid).first() 

        if not card: 
            return make_response(jsonify({"msg" : "Card doesn't exist"}), 201) 
        
        cardObj = {
                "id" : card.id, 
                "front" : card.front, 
                "back" : card.back, 
                "deck_id" : card.deck_id, 
                "user_id" : card.user_id
            }
        return make_response(jsonify(cardObj), 200 )

    
    def patch(self, cid): 
        """Updates selectively the card information
        Updates deck information also, updates last seen
        Returns 201 and error if error
        Returns 200 if success"""

        token = request.headers.get('token') 
        data = jwt.decode(token, app.config['SECRET_KEY'])

        user = User.query.filter_by(username = data['username']).first() 
        card = Card.query.filter_by(id = cid).first() 

        if not card or not user: 
            return make_response(jsonify({"error" : "Card doesn't exist"}), 201) 
        
        newCard = request.get_json()
        
        if not card.user_id == user.id: 
            return make_response(jsonify({"error" : "Please log in"}), 201)

        front = card.front
        if 'front' in newCard.keys(): 
            front = newCard['front'] 
        
        back = card.back
        if 'back' in newCard.keys(): 
            back = newCard['back'] 
        
        card.front = front
        card.back = back 

        #update last_seen
        Deck.query.filter_by(id = card.deck_id).first().last_seen = datetime.datetime.now()

        db.session.commit()

        return 200

    def delete(self, cid): 
        """Deletes the card from the data base
        If card doens't exist returns 201
        If user not logged in returns 201
        Returns 200 if succcess"""

        card = Card.query.filter_by(id = cid).first() 
        
        #card should exist 
        if not card: 
            return make_response(jsonify({"error" : "Card doesn't exist"}), 201) 
        
        #users can't make changes to whichever card they want
        token = request.headers.get('token') 
        data = jwt.decode(token, app.config['SECRET_KEY'])
        user = User.query.filter_by(username = data['username'])

        if not user.id == card.user_id: 
            return make_response(jsonify({"error" : "Please log in"}), 201) 

        Card.query.filter_by(id = cid).delete() 
        db.session.commit() 

        return 200
        
class specificCards(Resource): #deck/card/did
    @login_required
    def get(self, did):
        """Returns all the cards of a deck as array 
        201 if unsuccesful
        200 if ok"""
        
        #verifying if the request came from the logged in user for his own decks
        token = request.headers.get('token') 
        data = jwt.decode(token, app.config['SECRET_KEY'])

        user = User.query.filter_by(username = data['username']) 
        deck = Deck.query.filter_by(id = did).first() 
        if not deck or not deck.user_id == user.id: 
            return make_response(jsonify({"error" : "Deck doesn't exist or pls log in"}), 201 ) 

        cards = Card.query.filter_by(deck_id = did)
        output = []

        for card in cards: 
            cardObj = {} 

            cardObj = {
                "id" : card.id, 
                "front" : card.front, 
                "back" : card.back, 
                "deck_id" : card.deck_id, 
                "user_id" : card.user_id
            }

            output.append(cardObj)

        return make_response(jsonify(output), 200)

api.add_resource(allCards, '/card') 
api.add_resource(singleCard, '/card/<int:cid>')
api.add_resource(specificCards, '/deck/card/<int:did>')