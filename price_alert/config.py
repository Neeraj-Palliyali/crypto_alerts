from datetime import timedelta

DATABASES = {
       'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'krypto',
            'USER': 'postgres',
            'PASSWORD': 'ironman789',
            'HOST': 'localhost',
            'PORT': '5432',
       }
   }

ALLOWED_HOSTS = ["127.0.0.1",]

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=15),
    'ROTATE_REFRESH_TOKENS': True,
}

CELERY_BROKER_URL = 'sqla+postgresql://postgres:ironman789@localhost/krypto'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Kolkata'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'