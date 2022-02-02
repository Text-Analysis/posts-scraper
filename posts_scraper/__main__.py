import argparse as ap
from datetime import datetime

from posts_scraper.scraping.instagram import InstagramScraper


def setup_args_parser():
    parser = ap.ArgumentParser(
        description='Module for collecting information about user posts on Instagram and VK'
    )

    parser.add_argument(
        'username',
        type=str,
        help='the name of the social media account from which the data will be collected'
    )

    parser.add_argument(
        'password',
        type=str,
        help='the password of the social media account from which the data will be collected'
    )

    parser.add_argument(
        'target_username',
        type=str,
        help='the name of the social media account from which the data will be collected'
    )

    parser.add_argument(
        dest='since',
        type=str,
        help='the time since which the data will be collected (format: 2011-11-04)'
    )

    parser.add_argument(
        dest='until',
        type=str,
        help='the time until which the data will be collected (format: 2011-11-04)'
    )

    parser.add_argument(
        '-d',
        dest='dir',
        default='insta_data',
        type=str,
        help='the folder name for saving the collected information'
    )

    return parser


def main():
    parser = setup_args_parser()
    args = parser.parse_args()

    try:
        since = datetime.fromisoformat(args.since)
        until = datetime.fromisoformat(args.until)
    except ValueError as ex:
        print(ex)
        return

    scraper = InstagramScraper(args.username, args.password)
    posts = scraper.get_posts(args.target_username, since, until)

    for post in posts:
        print(post.json(ensure_ascii=False))


if __name__ == '__main__':
    main()
