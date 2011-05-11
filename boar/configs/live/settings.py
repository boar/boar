from boar.configs.staging.settings import *
import sys

MEDIA_ROOT = os.path.abspath(os.path.join(SITE_ROOT, '../../../media'))

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = 'http://media.theboar.org/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = 'http://media.theboar.org/admin/'

GOOGLE_MAPS_API_KEY = 'Set me in /etc/boar/local_settings.py'

FACEBOOK_API_KEY = 'Set me in /etc/boar/local_settings.py'
FACEBOOK_SECRET_KEY = 'Set me in /etc/boar/local_settings.py'

CACHE_BACKEND = 'memcached://127.0.0.1:11211/'

CELERY_BACKEND = 'cache'
BROKER_HOST = 'localhost'
BROKER_PORT = 5672
BROKER_USER = 'boar'
BROKER_PASSWORD = 'Set me in /etc/boar/local_settings.py'
BROKER_VHOST = 'boar'
CELERYBEAT_SCHEDULE_FILENAME = os.path.abspath(os.path.join(SITE_ROOT, '../../../celery/celerybeat-schedule'))

HAYSTACK_SOLR_URL = 'http://127.0.0.1:8180/solr'

sys.path.append('/etc/boar')
try:
    from local_settings import *
except ImportError:
    pass

