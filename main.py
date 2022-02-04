import logging
import logging.config
from time import sleep
from datetime import datetime

from instaloader import ProfileNotExistsException, ConnectionException

from configs import *
from scraping import InstagramScraper
from database import Database


def init_logger() -> logging.Logger:
    logging.config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger('my_logger')
    return logger


def main():
    logger = init_logger()

    target_input = input('Input username: ')
    since_input = input('Input since from date (format: 2022-01-20): ')
    until_input = input('Input until to date (format: 2022-01-20): ')
    try:
        since = datetime.fromisoformat(since_input)
        until = datetime.fromisoformat(until_input)
    except ValueError as ex:
        logger.fatal('exception occurred while converting since, until from strings to datetime objects: %s', ex)
        return

    if since > until:
        logger.fatal('until date cannot be earlier then since date: since=%s, until=%s', since, until)
        return

    connected = False
    while not connected:
        try:
            scraper = InstagramScraper(INSTA_LOGIN, INSTA_PASSWORD, logger)
            connected = True
        except ConnectionException as ex:
            logger.warning('exception occurred while getting %s account info: %s', target_input, ex)

            logger.info('sleep 10 second and retry to connect...')
            sleep(10)

    try:
        posts = scraper.get_posts(target_input, since, until)
    except ProfileNotExistsException as ex:
        logger.fatal('Exception occurred while getting %s account info: %s', target_input, ex)
        return

    db = Database(logger)
    db.add_posts_with_comments(posts)
    db.close_connection()


if __name__ == '__main__':
    main()
