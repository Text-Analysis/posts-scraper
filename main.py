import argparse as ap
import logging
import logging.config
from datetime import datetime
from time import sleep

from instaloader import ProfileNotExistsException, ConnectionException

from configs import *
from scraping import InstagramScraper


def init_logger() -> logging.Logger:
    logging.config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger('my_logger')
    return logger


def init_args_parser() -> ap.ArgumentParser:
    parser = ap.ArgumentParser(
        description='Python module for collecting information about user posts on Instagram '
                    'for the selected time period. The collected information is saved in the PostgreSQL database.'
    )

    parser.add_argument(
        'username',
        type=str,
        help='the account whose posts data will be saved into the PostgreSQL database'
    )

    parser.add_argument(
        'start_time',
        type=str,
        help='the beginning of the publication time period (in the format: 2022-01-01)'
    )

    parser.add_argument(
        'end_time',
        type=str,
        help='the end of the publication time period (in the format: 2022-01-01)'
    )

    return parser


def main():
    logger = init_logger()

    parser = init_args_parser()
    args = parser.parse_args()

    try:
        start_time = datetime.fromisoformat(args.start_time)
        end_time = datetime.fromisoformat(args.end_time)
    except ValueError as ex:
        logger.fatal('exception occurred while converting start_time, end_time from strings to datetime objects: %s',
                     ex)
        return

    if start_time > end_time:
        logger.fatal('end_time date cannot be earlier then start_time date: start_time=%s, end_time=%s',
                     start_time, end_time)
        return

    while True:
        try:
            scraper = InstagramScraper(INSTA_LOGIN, INSTA_PASSWORD, DATABASE_URL, logger)
            break
        except ConnectionException as ex:
            logger.warning('exception occurred while getting %s account info: %s', args.username, ex)

            logger.info('sleep 10 second and retry to connect...')
            sleep(10)

    try:
        scraper.scrape_posts(args.username, start_time, end_time)
    except ProfileNotExistsException as ex:
        logger.fatal('exception occurred while getting %s account info: %s', args.username, ex)
        return


if __name__ == '__main__':
    main()
