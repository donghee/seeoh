from celery.schedules import crontab
from datetime import timedelta

BROKER_URL = 'sqla+sqlite:///seeoh.sqlite'

CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = 'Asia/Seoul'
CELERYBEAT_SCHEDULE = {
  # Executes every Monday morning at 7:30 A.M
  'every-monday-morning': {
    'task': 'seeoh.tweet',
    'schedule': crontab(hour=7, minute=30, day_of_week=1),
    'args': (),
  },
  'runs-every-12-hours': {
    'task': 'seeoh.tweet',
    'schedule': timedelta(seconds=(3600*12)),
    'args': ()
  },
}

CELERY_IMPORTS = ("seeoh", )

#CELERY_RESULT_BACKEND = "database"
#CELERY_RESULT_DBURI = 'sqlite:///seeoh.sqlite'
#CELERY_RESULT_ENGINE_OPTIONS = {"echo": True}

CELERY_ANNOTATIONS = {"seeoh.tweet": {"rate_limit": "10/s"}}

