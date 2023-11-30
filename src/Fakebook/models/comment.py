from datetime import datetime
import MySQLdb.cursors


class Comment:
    def __init__(
        self,
        db = None,
        comment_id: int = 0,
        commenter_id: int = 0,
        commenter_name: str = "",
        text: str = "",
        creation_date: datetime = None,
        comment_replied_to: int = None
    ):
        self.db = db
        
        if db:
            self.cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

        self.comment_id = comment_id
        self.commenter_id = commenter_id
        self.commenter_name = commenter_name
        self.text = text
        self.creation_date = creation_date
        self.comment_replied_to = comment_replied_to

        self.replies = dict()

    def get_replies(self):
        cursor = self.cursor
        cursor.execute(
            "SELECT users_tb.username, comments_tb.comment_id, comments_tb.commenter_id, comments_tb.comment, comments_tb.creation_date, comments_tb.comment_replied_to FROM comments_tb INNER JOIN posts_tb ON comments_tb.post_id = posts_tb.post_id INNER JOIN users_tb ON users_tb.id = comments_tb.commenter_id WHERE posts_tb.post_id = %s ORDER BY comments_tb.creation_date DESC",
            (self.post_id,),
        )
        replies = cursor.fetchall()

        if replies:
            for reply in replies:
                item = Comment(
                    reply["comment_id"],
                    reply["commenter_id"],
                    reply["username"],
                    reply["comment"],
                    reply["creation_date"].strftime("%b %d, %Y %I:%M %p"),
                    reply["comment_replied_to"]
                )
                self.replies[reply["comment_id"]] = item
        else:
            return None
