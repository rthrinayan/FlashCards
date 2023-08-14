from TaskManager import celery, SENDGRID_API_KEY
from backend import *
import pandas as pd 
import os
import base64
import matplotlib
matplotlib.use('Agg') 
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import * 
import matplotlib.pyplot as plt 
from flask import render_template
import datetime

@celery.task
def monthlyReport(): 
    users =User.query.all()
    for user in users: 
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'history', str(user.id))
        try:
            df = pd.read_csv(filepath) 
            # datetime, no decks, no cards, avg score, rep

            X = df.iloc[:, 0] #datetime col
            dcount  = df.iloc[:,1] 
            ccount = df.iloc[:,2] 
            avg = df.iloc[:,3]
            rep = df.iloc[:,4]
            plt.plot(X, dcount, color='r', label='Decks') 
            plt.plot(X, ccount, color='b', label='Cards') 
            plt.plot(X, avg, color = 'g', label = 'Average Score') 
            plt.plot(X, rep, color='c', label = 'Reputation')
            plt.xlabel("Date") 
            plt.ylabel("Magnitude") 
            plt.title(f'Monthly report - {user.username}')
            plt.legend() 
            filename = filepath+ '.pdf'
            plt.savefig(filename, format='pdf')

            #sending picture as email 
            with app.app_context(): 
                output = render_template('report.html', name = user.username, score = user.reputation, filepath = f'../history/{user.id}.pdf')

                message = Mail(
                    from_email = '21f1003074@student.onlinedegree.iitm.ac.in',
                    to_emails=user.email, 
                    subject = f'Hey {user.username}! Here are your stats', 
                    html_content=output
                )
                
                with open(filename, 'rb') as f: 
                    data = f.read() 
                encoded_output = base64.b64encode(data).decode()

                attachedFile = Attachment(
                    FileContent(encoded_output), 
                    FileName('Monthly Report'), 
                    FileType('application/pdf'), 
                    Disposition('attachment')
                )
                message.attachment = attachedFile

                sg = SendGridAPIClient(SENDGRID_API_KEY) 
                response = sg.send(message) 
                print(response.status_code, response.body, response.headers)

            plt.clf() #so that multiple graphs don't overlay

        #if users history hasn't been made yet don't crash 
        except Exception as e: 
            print(e) 
            continue

        #creating the accumulated graph
    return 


@celery.task 
def reviseCheck(delt = 86400): #del corresponds to maximum allowable diff in time (seconds) 
    users = User.query.all()
    current_time = datetime.datetime.now() 
    for user in users: 
        decks = Deck.query.filter_by(user_id = user.id)
        if not decks: 
            continue
        last_seen = decks[0].last_seen
        seconds_passed = (current_time - last_seen).total_seconds()
        if seconds_passed > delt: 
            print('Bad User: ' , user.username, user.email)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'templates', 'revise.html')
            output = ''
            with app.app_context():
                output = render_template('revise.html', name = user.username, score = user.reputation)

            message = Mail(
                from_email = '21f1003074@student.onlinedegree.iitm.ac.in',
                to_emails=user.email, 
                subject = f'Hey {user.username}! How about a study session', 
                html_content=output
            )

            sg = SendGridAPIClient(SENDGRID_API_KEY) 
            response = sg.send(message) 
            print(response.status_code, response.body, response.headers)



@celery.task
def updateHistory(): # datetime, no decks, no cards, avg score, rep | and same for other categories 
    for user in User.query.all(): 
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'history') 
        filepath = os.path.join(filepath, str(user.id))
        file = open(filepath, 'a' ) 
        dcount = Deck.query.filter_by(user_id = user.id).count() 
        ccount = Card.query.filter_by(user_id = user.id).count()
        s=0
        for deck in Deck.query.filter_by(user_id = user.id):
            s += deck.score

        avg = 0 if not dcount else s/dcount 
        file.write(f'{datetime.datetime.now()}, {dcount}, {ccount}, {avg}, {user.reputation}\n')
        file.close() 

