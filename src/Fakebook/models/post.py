from .comment import Comment
from datetime import datetime
import MySQLdb.cursors


class Post:
    def __init__(
        self,
        db=None,
        post_id=0,
        user_id=0,
        creator_name="",
        description="",
        likes=0,
        creation_date: datetime = None,
    ):
        self.db = db
        self.cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

        self.post_id = post_id
        self.user_id = user_id
        self.creator_name = creator_name
        self.description = description
        self.likes = likes
        self.creation_date = creation_date

        self.__get_post()
        self.comments = self.__get_comments()
        
    def __get_post(self):
        cursor = self.cursor
        cursor.execute(
            "SELECT users_tb.username, posts_tb.user_id, posts_tb.description, posts_tb.likes, posts_tb.creation_date FROM posts_tb INNER JOIN users_tb ON posts_tb.user_id = users_tb.id WHERE posts_tb.post_id = %s",
            (
                self.post_id,
            ),
        )
        post = cursor.fetchone()
        
        if post:
            self.user_id = post['user_id']
            self.creator_name = post['username']
            self.description = post['description']
            self.likes = post['likes']
            self.creation_date = post['creation_date'].strftime("%b %d, %Y %I:%M %p")

    def __get_comments(self):
        cursor = self.cursor
        cursor.execute(
            "SELECT users_tb.username, comments_tb.comment_id, comments_tb.commenter_id, comments_tb.comment, comments_tb.creation_date, comments_tb.comment_replied_to FROM comments_tb INNER JOIN posts_tb ON comments_tb.post_id = posts_tb.post_id INNER JOIN users_tb ON users_tb.id = comments_tb.commenter_id WHERE posts_tb.post_id = %s ORDER BY comments_tb.creation_date DESC",
            (self.post_id,),
        )
        comments = cursor.fetchall()

        if comments:
            comments_list = []
            for comment in comments:
                item = Comment(
                    comment["comment_id"],
                    comment["commenter_id"],
                    comment["username"],
                    comment["comment"],
                    comment["creation_date"].strftime("%b %d, %Y %I:%M %p")
                )
                comments_list.append(item)
                
            return comments_list
        else:
            return None
