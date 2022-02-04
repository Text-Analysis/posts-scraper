from os import getenv
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

TZ = getenv('TZ')
DATABASE_URL = getenv('DATABASE_URL')
INSTA_LOGIN = getenv('INSTAGRAM_LOGIN')
INSTA_PASSWORD = getenv('INSTAGRAM_PASSWORD')

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'default_formatter': {
            'format': '[%(levelname)s] %(message)s'
        },
    },

    'handlers': {
        'stream_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'default_formatter',
        },
    },

    'loggers': {
        'my_logger': {
            'handlers': ['stream_handler'],
            'level': 'INFO',
            'propagate': False
        }
    }
}
