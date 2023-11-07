from .datatypes import Name, Address
from .person import Person
from .timeline import Timeline
from datetime import datetime
import MySQLdb.cursors


class User(Person):
    def __init__(self, db, user_id: int):
        self.db = db
        self.cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

        self.user_id = user_id
        self.username = ""
        self.creation_date: datetime = None
        self.profile_picture_url = ""

        self.timeline = Timeline(db, user_id)

        self.__get_user()

    def __get_user(self):
        cursor = self.cursor
        cursor.execute(
            "SELECT * FROM fakebook_db.users_tb WHERE id = %s",
            (self.user_id,),
        )
        user = cursor.fetchone()

        if user:
            self.username = user["username"]
            self.email = user["email"]
            self.phone = user["phone"]
            self.profile_picture_url = user["profile_picture_url"]
            self.gender = user["gender"]
            self.name = Name(user["first_name"], user["middle_name"], user["last_name"])
            self.address = Address(
                user["street"],
                user["city"],
                user["state"],
                user["country"],
                user["zipcode"],
            )
            self.date_of_birth = user[
                "date_of_birth"
            ]  # .strftime("%b %d, %Y %I:%M %p")
            self.creation_date = user["creation_date"]

    def make_post(self, post_description: str):
        db = self.db
        cursor = db.connection.cursor()
        creation_date = datetime.now()

        # Create post
        cursor.execute(
            "INSERT INTO posts_tb (user_id, description, creation_date) VALUES(%s, %s, %s)",
            (
                self.user_id,
                post_description,
                creation_date,
            ),
        )

        # Get post id from newly created post
        cursor.execute("SELECT LAST_INSERT_ID()")
        post_id = cursor.fetchone()

        # Create table to check whether user has liked a post or not. Default is not liked.
        cursor.execute(
            "INSERT INTO liked_posts_tb (liked_post_id, liked_user_id) VALUES(%s, %s)",
            (
                post_id,
                self.user_id,
            ),
        )

        db.connection.commit()
        db.connection.close()

    def like_post(self, post_id: int):
        db = self.db
        cursor = self.cursor
        cursor.execute(
            "UPDATE posts_tb INNER JOIN liked_posts_tb ON posts_tb.post_id = liked_posts_tb.liked_post_id SET posts_tb.likes = posts_tb.likes + 1, liked_posts_tb.liked_status = 1 WHERE posts_tb.post_id = %s AND posts_tb.user_id = %s AND liked_posts_tb.liked_status = 0",
            (
                post_id,
                self.user_id,
            ),
        )

        db.connection.commit()
        db.connection.close()

    def make_comment():
        pass

    def send_friend_request():
        pass
