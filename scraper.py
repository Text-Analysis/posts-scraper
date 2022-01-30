import argparse as ap
from itertools import takewhile, dropwhile
from datetime import datetime

from instaloader import Instaloader, Profile


def setup_args_parser():
    parser = ap.ArgumentParser(
        description="Module for collecting information about user posts on Instagram"
    )

    parser.add_argument(
        "username",
        type=str,
        help="the name of the Instagram account from which the data will be collected"
    )

    parser.add_argument(
        "password",
        type=str,
        help="the password of the Instagram account from which the data will be collected"
    )

    parser.add_argument(
        "target_username",
        type=str,
        help="the name of the Instagram account from which the data will be collected"
    )

    parser.add_argument(
        dest="since",
        type=str,
        help="the time since which the data will be collected (format: 2011-11-04)"
    )

    parser.add_argument(
        dest="until",
        type=str,
        help="the time until which the data will be collected (format: 2011-11-04)"
    )

    parser.add_argument(
        "-d",
        dest="dir",
        default="insta_data",
        type=str,
        help="the folder name for saving the collected information"
    )

    return parser


def main():
    parser = setup_args_parser()
    args = parser.parse_args()

    loader = Instaloader(
        download_comments=True,
        download_pictures=True,
        download_videos=False,
        download_video_thumbnails=False,
        download_geotags=False,
        save_metadata=False,
        dirname_pattern=args.dir
    )
    loader.login(args.username, args.password)

    posts = Profile.from_username(loader.context, args.target_username).get_posts()

    try:
        since = datetime.fromisoformat(args.since)
        until = datetime.fromisoformat(args.until)
    except ValueError as ex:
        print(ex)
        return

    for post in takewhile(lambda p: p.date > since, dropwhile(lambda p: p.date > until, posts)):
        loader.download_post(post, args.target_username)


if __name__ == "__main__":
    main()
