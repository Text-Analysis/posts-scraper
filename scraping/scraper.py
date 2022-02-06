from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List, TypeVar

import instaloader

from scraping.models import PostScrapingModel, CommentScrapingModel

SocialnetPost = TypeVar('SocialnetPost', bound=instaloader.Post)


class Scraper(ABC):

    @abstractmethod
    def get_posts(self, username: str,
                  since: datetime = (datetime.now() - timedelta(30)),
                  until: datetime = datetime.now()
                  ) -> List[PostScrapingModel]:
        """
        :param username: the scraper target
        :param since: beginning of period
        :param until: end of period
        :return: a list of posts
        """
        pass

    @abstractmethod
    def get_comments(self, post: SocialnetPost) -> List[CommentScrapingModel]:
        """
        :param post: represents social media post
        :return: a list of post's comments
        """
        pass
