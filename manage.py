from pytz import timezone

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore, MongoClient
from apscheduler.executors.pool import ThreadPoolExecutor

from appname import create_app


app = create_app('appname.config.BaseConfig')

jobstores = {
        'default': MongoDBJobStore(client=MongoClient(app.config.get('MONGO_URI'))),
}
executors = {
        'default': ThreadPoolExecutor(20)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 5
}
scheduler_tz = timezone(app.config["TIME_ZONE"])
scheduler = BackgroundScheduler(jobstores=jobstores,
                                executors=executors,
                                job_defaults=job_defaults,
                                timezone=scheduler_tz)
scheduler.start()

app.scheduler = scheduler
