from TaskManager import celery 
import TaskManager
from celery.schedules import crontab 

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        # crontab(hour=9, minute=0, day_of_week='*'), #updating history files every day
        10.0, #for testing purposes  
        TaskManager.updateHistory.s() 
    )
    sender.add_periodic_task(
        # crontab(hour=12, minute=30, day_of_week='*'), #checking for non-revisers every day
        30.0, #for testing purposes
        TaskManager.reviseCheck.s()
    )
    sender.add_periodic_task(
        # crontab(minute = 30, hour = 12, day_of_month=0), #generating monthly report once a month 
        100.0,#for testing purposes
        TaskManager.monthlyReport.s()
    )