from os import getenv

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

TZ = getenv('TZ')
DATABASE_URL = getenv('DATABASE_URL')
INSTA_LOGIN = getenv('INSTAGRAM_LOGIN')
INSTA_PASSWORD = getenv('INSTAGRAM_PASSWORD')
