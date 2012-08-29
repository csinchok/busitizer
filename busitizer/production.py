import os
from busitizer.settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

# OK, this is silly, but I'm gonna do it.
pgpass_file = open('/home/fabric/.pgpass')
pgpass = pgpass_file.read()[:-1].split(":")
pgpass_file.close()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': pgpass[1],
        'USER': pgpass[2],
        'PASSWORD': pgpass[3],
        'HOST': pgpass[0],
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

MEDIA_URL = 'http://static.busitizer.com/media/'
STATIC_URL = 'http://static.busitizer.com/static/'

CELERY_ALWAYS_EAGER = FalseCELERY_ALWAYS_EAGER = False
THUMBNAIL_DUMMY = False
