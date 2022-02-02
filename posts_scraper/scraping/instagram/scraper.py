from datetime import datetime, timedelta
from itertools import takewhile, dropwhile
from typing import List
from pytz import timezone

from instaloader import Instaloader, Profile, Post

from posts_scraper.scraping.models import CommentScrapingModel, PostScrapingModel
from posts_scraper.scraping.scraper import Scraper
from posts_scraper.configs.configs import TZ


class InstagramScraper(Scraper):

    def __init__(self, login: str, password: str):
        self.loader = Instaloader()
        self.loader.login(login, password)

    def get_posts(self, username: str,
                  since=(datetime.now() - timedelta(30)),
                  until=datetime.now()
                  ) -> List[PostScrapingModel]:
        profile = Profile.from_username(self.loader.context, username)
        posts = profile.get_posts()

        scraped_posts: List[PostScrapingModel] = []
        for post in takewhile(lambda p: p.date > since, dropwhile(lambda p: p.date > until, posts)):
            post_comments = self.get_comments(post)
            post_url = f'https://www.instagram.com/p/{post.shortcode}/'
            post_owner_url = f'https://www.instagram.com/{post.owner_username}/'

            scraped_posts.append(PostScrapingModel(
                url=post_url,
                owner_url=post_owner_url,
                picture=post.url,
                text=post.caption,
                likes=post.likes,
                created_at_time=post.date_local.replace(tzinfo=timezone(TZ)),
                comments=post_comments
            ))
        return scraped_posts

    @staticmethod
    def get_comments(post: Post) -> List[CommentScrapingModel]:
        post_url = f'https://www.instagram.com/p/{post.shortcode}/'

        scraped_comments: List[CommentScrapingModel] = []
        for comment in post.get_comments():
            scraped_comment = CommentScrapingModel(
                url=f'{post_url}c/{comment.id}/',
                owner_url=f'https://www.instagram.com/{comment.owner.username}/',
                post_url=post_url,
                text=comment.text,
                likes=comment.likes_count,
                created_at_time=comment.created_at_utc.replace(tzinfo=timezone(TZ)),
            )
            scraped_comments.append(scraped_comment)

            for answer in comment.answers:
                scraped_comments.append(CommentScrapingModel(
                    url=f'{scraped_comment.url}r/{answer.id}/',
                    owner_url=f'https://www.instagram.com/{answer.owner.username}/',
                    post_url=post_url,
                    text=answer.text,
                    likes=answer.likes_count,
                    created_at_time=comment.created_at_utc.replace(tzinfo=timezone(TZ)),
                ))
        return scraped_comments
