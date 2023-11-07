from .comment import Comment
from datetime import datetime


class Post:
    def __init__(
        self,
        post_id=0,
        user_id=0,
        description="",
        likes=0,
        creation_date: datetime = None,
    ):
        self.post_id = post_id
        self.user_id = user_id
        self.description = description
        self.likes = likes
        self.creation_date = creation_date
        self.comments = Comment()
        