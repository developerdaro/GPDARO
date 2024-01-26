from .base import *

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db_gpdaro.sqlite',
    }
}

STATIC_ROOT = 'static'
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = '/media/'
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
