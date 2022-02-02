from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List
from models import PostScrapingModel, CommentScrapingModel
from instaloader import Post


class Scraper(ABC):

    @abstractmethod
    def get_posts(self, username: str,
                  since: datetime = (datetime.now() - timedelta(30)),
                  until: datetime = datetime.now()
                  ) -> List[PostScrapingModel]:
        """
        :param username: account
        :param since: beginning of period
        :param until: end of period
        :return: Method returns a list of posts
        """
        pass
