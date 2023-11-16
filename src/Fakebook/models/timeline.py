from .post import Post
import MySQLdb.cursors


class Timeline:
    def __init__(self, db, user_id: int):
        self.db = db
        self.cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

        self.user_id = user_id
        self.posts = dict()

    def view_timeline(self):
        cursor = self.cursor
        cursor.execute(
            "SELECT posts_tb.* FROM posts_tb WHERE posts_tb.user_id = %s OR posts_tb.user_id IN (SELECT friend_accepter_id FROM friends_tb WHERE friend_requester_id = %s) ORDER BY posts_tb.creation_date DESC",
            (
                self.user_id,
                self.user_id,
            ),
        )
        posts = cursor.fetchall()

        if posts:
            for post in posts:
                item = Post(self.db, post["post_id"])
                self.posts[post["post_id"]] = item
        else:
            return None
