from backend import app

if __name__  == '__main__': 
    app.run(debug = True) 

#celery -A tasks.celery worker -l INFO