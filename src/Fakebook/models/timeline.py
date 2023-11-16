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
            "SELECT * FROM (SELECT * FROM posts_tb WHERE user_id = %s UNION SELECT posts_tb.* FROM posts_tb INNER JOIN friends_tb ON posts_tb.user_id = friends_tb.friend_requester_id WHERE friends_tb.friend_accepter_id = %s AND friends_tb.friend_request_status = 'ACCEPTED' UNION SELECT posts_tb.* FROM posts_tb INNER JOIN friends_tb ON posts_tb.user_id = friends_tb.friend_accepter_id WHERE friends_tb.friend_requester_id = %s AND friends_tb.friend_request_status = 'ACCEPTED') AS combined_result ORDER BY combined_result.creation_date DESC",
            (
                self.user_id,
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
