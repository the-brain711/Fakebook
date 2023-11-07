from .post import Post
import MySQLdb.cursors


class Timeline:
    def __init__(self, db, user_id: int):
        self.db = db
        self.cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

        self.user_id = user_id
        self.posts = []

    def view_timeline(self):
        cursor = self.cursor
        cursor.execute(
            "SELECT users_tb.username, posts_tb.* FROM posts_tb INNER JOIN users_tb ON posts_tb.user_id = users_tb.id WHERE posts_tb.user_id = %s ORDER BY posts_tb.creation_date DESC",
            (self.user_id,),
        )
        posts = cursor.fetchall()

        if posts:
            for post in posts:
                item = Post(self.db, post["post_id"])
                self.posts.append(item)

            return self.posts

        else:
            return None
