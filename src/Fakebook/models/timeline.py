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
        

        for post in posts:
            post["creation_date"] = post["creation_date"].strftime("%b %d, %Y %I:%M %p")

            item = Post(
                post["post_id"],
                post["user_id"],
                post["description"],
                post["likes"],
                post["creation_date"],
            )
            self.posts.append(item)

        return self.posts