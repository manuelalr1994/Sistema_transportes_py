from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['www.transportesgsmo.com', 'transportesgsmo.com']
CSRF_TRUSTED_ORIGINS = ['https://www.transportesgsmo.com', 'https://transportesgsmo.com']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR.child('static')]
STATIC_ROOT = BASE_DIR.child('staticfiles')

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'EA',
        'USER': 'postgres',
        'PASSWORD': 'Lema50411',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

