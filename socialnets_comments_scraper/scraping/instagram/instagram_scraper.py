from typing import List

from instaloader import Instaloader, Profile

from socialnets_comments_scraper.models import Comment


class InstagramScraper:
    def __init__(self, login: str, password: str):
        self.loader = Instaloader()
        self.loader.login(login, password)

    def get_comments(self, username: str) -> List[Comment]:
        prof = Profile.from_username(self.loader.context, username)
        posts = prof.get_posts()

        comments: List[Comment] = []
        for post in posts:
            for comment in post.get_comments():
                comment_correct = Comment(
                    Id=comment.id,
                    PostId=post.shortcode,
                    Text=comment.text,
                    UrlUser=comment.owner.username,
                    Time=comment.created_at_utc,
                    Tags=[],
                    Links=[]
                )
                comments.append(comment_correct)

        return comments
