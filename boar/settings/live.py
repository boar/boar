from __future__ import absolute_import
import sys

from .base import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

MEDIA_ROOT = '/var/www/theboar.org/media/'

GOOGLE_MAPS_API_KEY = 'Set me in live_secret.py'
FACEBOOK_API_KEY = 'Set me in live_secret.py'
FACEBOOK_SECRET_KEY = 'Set me in live_secret.py'

CACHE_BACKEND = 'redis_cache.cache://127.0.0.1:6379/?timeout=5'

CELERY_ALWAYS_EAGER = False
CELERY_RESULT_BACKEND = 'redis'
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = '0'
BROKER_BACKEND = 'redis'
BROKER_HOST = 'localhost'
BROKER_PORT = 6379
BROKER_VHOST = '0'
CELERYBEAT_SCHEDULE_FILENAME = '/var/www/theboar.org/celery/celerybeat-schedule'

HAYSTACK_SOLR_URL = 'http://127.0.0.1:8080/solr'

GIT_REVISION = '%(GIT_REVISION)s'

from .live_secret import *

