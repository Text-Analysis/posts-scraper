from datetime import datetime

from instaloader import ProfileNotExistsException

from configs import *
from scraping.instagram import InstagramScraper


def main():
    target_input = input('Input username: ')

    since_input = input('Input since from date: ')
    until_input = input('Input until to date: ')
    try:
        since = datetime.fromisoformat(since_input)
        until = datetime.fromisoformat(until_input)
    except ValueError as ex:
        print('Exception occurred while converting since, until from strings to datetime objects:', ex)
        return

    scraper = InstagramScraper(INSTA_LOGIN, INSTA_PASSWORD)

    try:
        posts = scraper.get_posts(target_input, since, until)
    except ProfileNotExistsException as ex:
        print(f'Exception occurred while getting {target_input} posts: ', ex)
        return

    for post in posts:
        print(post.json(ensure_ascii=False))


if __name__ == '__main__':
    main()
