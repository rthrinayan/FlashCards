from backend.flashcards import *
from backend import db, app
import datetime
from backend import * #to avoid circular imports
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import * 
import base64
from TaskManager import celery, SENDGRID_API_KEY

#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


@celery.task #handling import for cards
def addCards(filename, uid): 
    
    #reading the upload folder as df to be able to add cards to new deck 
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'templates', str(uid))
    file = open(file_path, 'r') 
    lines = file.readlines() 
    values = []

    for line in lines:
        if line == lines[0]: 
            continue #we don't want the headers

        l = line.strip() 
        print(l)  
        f, b = l.split(', ')
        values.append([f, b])
    print(values) 
    last_seen = datetime.datetime.now()
    deck = Deck(
        name = filename, 
        description = "Imported Deck", 
        last_seen = last_seen, 
        user_id = uid
    )
    db.session.add(deck)
    db.session.commit() 
    did = Deck.query.filter((Deck.user_id == uid) & (Deck.last_seen == last_seen)).first().id 
    for row in values: #making each card and committing
        front, back = row[0], row[1] 
        card = Card(
            front = front, 
            back = back, 
            deck_id = did, 
            user_id = uid
        )

        db.session.add(card) 
        db.session.commit() 
    db.session.commit()
    return 


@celery.task #handling exports, being sent to emails
def sendCards(did, uid, csv = None, html = None):
    user = User.query.filter_by(id = uid).first() 
    deck = Deck.query.filter_by(id = did).first()
    message = Mail(
        from_email = '21f1003074@student.onlinedegree.iitm.ac.in',
        to_emails = user.email,
        subject = f'Exporting {deck.name} as a csv and html file', 
        plain_text_content='Please find below the attachments of the deck in the formats of csv and html', 
    )

    data = csv if csv else html
    encoded_output = base64.b64encode(data.encode("ascii")).decode() 
    filename = f'{deck.name}.csv' if csv else f'{deck.name}.html'

    attachedFile = Attachment(
        FileContent(encoded_output), 
        FileName(filename), 
        FileType('text/html'), 
        Disposition('attachment')
    )

    message.attachment = attachedFile 

    sg = SendGridAPIClient(SENDGRID_API_KEY)
    response = sg.send(message)
    print(response.status_code, response.body, response.headers)
