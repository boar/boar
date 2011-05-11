from boar.configs.settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = 'http://staging-media.theboar.org/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = 'http://staging-media.theboar.org/admin/'

COMPRESS = True
COMPRESS_AUTO = False
COMPRESS_VERSION = True

CELERY_ALWAYS_EAGER = False

#SESSION_COOKIE_DOMAIN = '.theboar.org'
