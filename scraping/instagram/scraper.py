from datetime import timedelta
from itertools import takewhile, dropwhile
from time import sleep

from instaloader import Instaloader, Profile
from pytz import timezone

from configs import TZ
from database import Database
from models import *
from scraping.scraper import Scraper
from utility import *


class InstagramScraper(Scraper):

    def __init__(self, login: str, password: str, database_url: str):
        self.db = Database(database_url)

        self.loader = Instaloader()
        self.loader.login(login, password)

    def scrape_posts(self, username: str,
                     since=(datetime.now() - timedelta(30)),
                     until=datetime.now()
                     ) -> List[PostScrapingModel]:
        profile = Profile.from_username(self.loader.context, username)
        sleep(10)

        account_info = AccountScrapingModel(
            url=f'https://www.instagram.com/{profile.username}/',
            entity=EntityScrapingModel(
                name=profile.full_name,
                is_organization=profile.is_business_account
            ),
            socialnet=SocialnetScrapingModel(
                name='Instagram'
            )
        )

        self.db.update_account(account_info)
        print('account information has been scraped: %s', account_info.url)

        posts = profile.get_posts()
        sleep(10)

        scraped_posts: List[PostScrapingModel] = []
        for post in takewhile(lambda p: p.date >= since, dropwhile(lambda p: p.date >= until, posts)):
            post_comments = self.scrape_comments(post)
            sleep(3)

            post_info = PostScrapingModel(
                url=f'https://www.instagram.com/p/{post.shortcode}/',
                account=account_info,
                picture=post.url,
                text=post.caption,
                likes=post.likes,
                time=post.date_local.replace(tzinfo=timezone(TZ)),
                comments=post_comments,
                tags=post.caption_hashtags,
                links=post.caption_mentions
            )

            scraped_posts.append(post_info)
            print('post information has been scraped: %s', post_info.url)
            sleep(3)

            post_from_db = self.db.update_post(post_info)
            for post_comment in post_comments:
                self.db.update_comment(post_comment, post_from_db.id)
            sleep(3)

        self.db.close_connection()

        return scraped_posts

    def scrape_comments(self, post: Post) -> List[CommentScrapingModel]:
        post_url = f'https://www.instagram.com/p/{post.shortcode}/'

        scraped_comments: List[CommentScrapingModel] = []
        for comment in post.get_comments():
            comment_info = CommentScrapingModel(
                url=f'{post_url}c/{comment.id}/',
                owner_url=f'https://www.instagram.com/{comment.owner.username}/',
                post_url=post_url,
                text=comment.text,
                likes=comment.likes_count,
                time=comment.created_at_utc.replace(tzinfo=timezone(TZ)),
                tags=get_hashtags(comment.text),
                links=get_mentions(comment.text)
            )

            scraped_comments.append(comment_info)
            print('comment information has been scraped: %s', comment_info.url)
            sleep(3)

            for answer in comment.answers:
                answer_info = CommentScrapingModel(
                    url=f'{comment_info.url}r/{answer.id}/',
                    owner_url=f'https://www.instagram.com/{answer.owner.username}/',
                    post_url=post_url,
                    text=answer.text,
                    likes=answer.likes_count,
                    time=answer.created_at_utc.replace(tzinfo=timezone(TZ)),
                    tags=get_hashtags(answer.text),
                    links=get_mentions(answer.text)
                )

                scraped_comments.append(answer_info)
                print('answer information has been scraped: %s', answer_info.url)
                sleep(3)

        return scraped_comments
