from celery import Celery 
celery = Celery('TaskManager', broker='redis://localhost:6379', backend = 'redis://localhost:6380') 
SENDGRID_API_KEY = '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'

from TaskManager.beatConfig import *
from TaskManager.flashcardTasks import * 
from TaskManager.recurrentTasks import *