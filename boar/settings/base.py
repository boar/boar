# Django settings for boar project.

import os, django, boar
DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
SITE_ROOT = os.path.dirname(os.path.realpath(boar.__file__))

######################################
# Main
######################################

DEBUG = True
ROOT_URLCONF = 'boar.urls'

######################################
# Site
######################################

SITE_ID = 1
SECRET_KEY = 'Set me with base_secret.py'
APPEND_SLASH = True

# Git revision, set in fabfile.py with a local_settings.py file
GIT_REVISION = 'unknown'

######################################
# Apps
######################################

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.comments',
    'django.contrib.contenttypes',
    'django.contrib.flatpages',
    'django.contrib.gis',
    'django.contrib.humanize',
    'django.contrib.markup',
    'django.contrib.sessions',
    'django.contrib.sites',
    
    'celery',
    'compressor',
    'debug_toolbar',
    'django_inlines',
    'haystack',
    'pagination',
    'reversion',
    'shorturls',
    'sorl.thumbnail',
    'south',
    'taggit',
    'threadedcomments',
    'typogrify',
    
    'boar.accounts',
    'boar.archive',
    'boar.articles',
    'boar.awards',
    'boar.cacher',
    'boar.cartoons',
    'boar.comments_extra',
    'boar.common',
    'boar.editorial_board',
    'boar.facebook_connect',
    'boar.mailing_lists',
    'boar.search',
    'boar.uploads',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware', # first
    'django.middleware.transaction.TransactionMiddleware', # second
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfMiddleware',
    'boar.articles.middleware.ArticleMiddleware', # before cacher
    'boar.cacher.middleware.CachedPageMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'boar.facebook_connect.middleware.FacebookConnectMiddleware', # after auth
    'reversion.middleware.RevisionMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware', # last
)

######################################
# APIs
######################################

GOOGLE_MAPS_API_KEY = 'Set me with local_settings.py'
RECAPTCHA_PUBLIC_KEY = 'Set me with local_settings.py'
RECAPTCHA_PRIVATE_KEY = 'Set me with local_settings.py'
TWITTER_USERNAME = 'Set me with local_settings.py'
TWITTER_PASSWORD = 'Set me with local_settings.py'

######################################
# Auth
######################################

ACCOUNT_ACTIVATION_DAYS = 30
AUTH_PROFILE_MODULE = 'accounts.userprofile'
LOGIN_URL = '/accounts/'

######################################
# Cache
######################################

CACHE_BACKEND = 'dummy:///'
CACHED_PAGES = [
    '/',
    '/news/',
    '/comment/',
    '/features/',
    '/money/',
    '/science/',
    '/lifestyle/',
    '/travel/',
    '/books/',
    '/film/',
    '/arts/',
    '/tv/',
    '/music/',
    '/games/',
    '/sport/',
    '/about/',
]

CACHED_BITS = {
    'MESSAGES': 'accounts/snippets/messages.html',
}

######################################
# Celery
######################################

CELERYD_CONCURRENCY = 5
CELERY_ALWAYS_EAGER = True

######################################
# Comments
######################################

COMMENTS_ALLOW_PROFANITIES = True
COMMENTS_APP = 'boar.comments_extra'

######################################
# Database
######################################

DATABASES = {
    'default': {
        'NAME': 'boar',
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'USER': '',
        'PASSWORD': ''
    },
}

POSTGIS_SQL_PATH = '/usr/share/postgresql-8.3-postgis'

######################################
# Debug toolbar
######################################

def show_toolbar_callback(request):
    from django.conf import settings
    #settings.DEBUG_TOOLBAR_CONFIG['SHOW_TEMPLATE_CONTEXT'] = 'debug-context' in request.GET
    
    return settings.DEBUG and ('__debug__' in request.path or 'debug' in request.GET)
    # TODO: return settings.DEBUG and not 'nodebug' in request.GET
    
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': show_toolbar_callback,
    #'SHOW_TEMPLATE_CONTEXT': False,
    'INTERCEPT_REDIRECTS': False,
}

######################################
# Email
######################################

ADMINS = (
    ('Technical Manager', 'tech@theboar.org'),
)

MANAGERS = ADMINS

DEFAULT_FROM_EMAIL = 'tech@theboar.org'
EMAIL_SUBJECT_PREFIX = '[Boar] '
SERVER_EMAIL = 'tech@theboar.org'

######################################
# Facebook
######################################

FACEBOOK_API_KEY = 'Set me with local_settings.py'
FACEBOOK_SECRET_KEY = 'Set me with local_settings.py'

######################################
# Inlines
######################################

INLINE_DEBUG = DEBUG

######################################
# Localisation
######################################

# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'Europe/London'
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-gb'
USE_I18N = False

######################################
# Media
######################################

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(SITE_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/admin/'

COMPRESS = True
COMPRESS_CSS_FILTERS = ['boar.common.compress_filters.CleverCSSFilter']
COMPRESS_JS_FILTERS = []

######################################
# Search
######################################

HAYSTACK_SEARCH_ENGINE = 'solr'
HAYSTACK_SOLR_URL = 'http://127.0.0.1:8983/solr'
HAYSTACK_SITECONF = 'boar.search_sites'

######################################
# Short URLs
######################################

SHORTEN_MODELS = {
    'a': 'articles.article',
    'u': 'auth.user',
}
SHORTURLS_DEFAULT_CONVERTER = 'shorturls.baseconv.base32'

######################################
# South
######################################

SOUTH_AUTO_FREEZE_APP = True
SOUTH_TESTS_MIGRATE = True
SKIP_SOUTH_TESTS = True

######################################
# Templates
######################################

TEMPLATE_DEBUG = DEBUG
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
TEMPLATE_DIRS = (
    os.path.join(SITE_ROOT, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.csrf',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'boar.common.context_processors.default_section',
    'boar.facebook_connect.context_processors.facebook_api_key',
    'boar.common.context_processors.google_maps_api_key',
    'boar.common.context_processors.git_revision',
)

######################################
# Tests
######################################

TEST_RUNNER='django.contrib.gis.tests.run_tests'


######################################
# Uploads
######################################

UPLOAD_DIRECTORY='uploads/%Y/%m/%d'


try:
    from .base_secret import *
except ImportError:
    pass

