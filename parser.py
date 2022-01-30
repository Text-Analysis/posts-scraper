import instaloader
from typing import List
from schemas.schemas import Comment


class Parser:

    def __init__(self, username: str, password: str):
        self.loader = instaloader.Instaloader()
        self.loader.login(username, password)

    def get_comments(self, username: str) -> List[Comment]:
        prof = instaloader.Profile.from_username(self.loader.context, username)
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
