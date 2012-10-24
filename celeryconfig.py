from celery.schedules import crontab
from datetime import timedelta

BROKER_URL = 'sqla+sqlite:///seeoh.sqlite'

CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = 'Asia/Seoul'
CELERYBEAT_SCHEDULE = {
  'every-six-hours': {
    'task': 'seeoh.tweet',
    'schedule': crontab(hour='7,13,19', minute=30),
    'args': (),
  },
  # 'every-minute': {
    # 'task': 'seeoh.tweet',
    # 'schedule': crontab(minute='*'),
    # 'args': (),
  # },
}

CELERY_IMPORTS = ("seeoh", )

CELERY_ANNOTATIONS = {"seeoh.tweet": {"rate_limit": "10/s"}}

