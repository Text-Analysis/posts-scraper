import logging
from datetime import timedelta
from itertools import takewhile, dropwhile
from pytz import timezone
from time import sleep

from instaloader import Instaloader, Profile, Post

from scraping.models import *
from scraping.scraper import Scraper
from configs.configs import TZ


class InstagramScraper(Scraper):

    def __init__(self, login: str, password: str, logger: logging.Logger):
        self.loader = Instaloader()
        self.loader.login(login, password)
        self.logger = logger

    def get_account_info(self, username: str) -> AccountScrapingModel:
        profile = Profile.from_username(self.loader.context, username)

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

        self.logger.info('account information has been scraped: %s', account_info)
        return account_info

    def get_posts(self, username: str,
                  since=(datetime.now() - timedelta(30)),
                  until=datetime.now()
                  ) -> List[PostScrapingModel]:
        profile = Profile.from_username(self.loader.context, username)

        account = self.get_account_info(username)
        sleep(3)

        posts = profile.get_posts()
        sleep(3)

        scraped_posts: List[PostScrapingModel] = []
        for post in takewhile(lambda p: p.date >= since, dropwhile(lambda p: p.date >= until, posts)):
            post_comments = self.get_comments(post)

            post_info = PostScrapingModel(
                url=f'https://www.instagram.com/p/{post.shortcode}/',
                account=account,
                picture=post.url,
                text=post.caption,
                likes=post.likes,
                time=post.date_local.replace(tzinfo=timezone(TZ)),
                comments=post_comments
            )

            scraped_posts.append(post_info)
            self.logger.info('post information has been scraped: %s', post_info)
            sleep(3)

        return scraped_posts

    def get_comments(self, post: Post) -> List[CommentScrapingModel]:
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
            )

            scraped_comments.append(comment_info)
            self.logger.info('comment information has been scraped: %s', comment_info)
            sleep(3)

            for answer in comment.answers:
                answer_info = CommentScrapingModel(
                    url=f'{comment_info.url}r/{answer.id}/',
                    owner_url=f'https://www.instagram.com/{answer.owner.username}/',
                    post_url=post_url,
                    text=answer.text,
                    likes=answer.likes_count,
                    time=comment.created_at_utc.replace(tzinfo=timezone(TZ)),
                )

                scraped_comments.append(answer_info)
                self.logger.info('answer information has been scraped: %s', answer_info)
                sleep(3)

        return scraped_comments
