import os

TZ = os.environ.get('TZ')

DATABASE = {
    'USER': os.environ.get('POSTGRES_USER'),
    'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
}

INSTA_LOGIN = os.environ.get('INSTAGRAM_LOGIN')
INSTA_PASSWORD = os.environ.get('INSTAGRAM_PASSWORD')
