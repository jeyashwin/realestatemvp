from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.base import STATE_STOPPED
from django.conf import settings

scheduler = BackgroundScheduler()

def startScheduler():
    """Function to start background Scheduler"""
    # print(scheduler.state)
    if scheduler.state == STATE_STOPPED:
        url = 'postgres://{}:{}@{}:{}/{}'.format(
                settings.DATABASES['default']['USER'],
                settings.DATABASES['default']['PASSWORD'],
                settings.DATABASES['default']['HOST'],
                settings.DATABASES['default']['PORT'],
                settings.DATABASES['default']['NAME']
                )
        scheduler.add_jobstore('sqlalchemy', url=url, tablename="taskstore")
        scheduler.start()