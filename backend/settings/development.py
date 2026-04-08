import os
from dotenv import load_dotenv
from .base import *

load_dotenv()

SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-dev-only-change-in-production'
)

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

CORS_ALLOW_ALL_ORIGINS = True
