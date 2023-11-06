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
            self.date_of_birth = user["date_of_birth"] # .strftime("%b %d, %Y %I:%M %p")
            self.creation_date = user["creation_date"]

    def make_post(self, post_description: str):
        db = self.db
        cursor = self.cursor
        creation_date = datetime.now()

        cursor.execute(
            "INSERT INTO posts_tb (user_id, description, creation_date) VALUES(%s, %s, %s)",
            (
                self.user_id,
                post_description,
                creation_date,
            ),
        )

        db.connection.commit()
        db.connection.close()

    def like_post(self, post_id: int):
        db = self.db
        cursor = self.cursor
        cursor.execute(
            "UPDATE posts_tb SET likes = likes + 1 WHERE post_id = %s;",
            (post_id,),
        )

        db.connection.commit()
        db.connection.close()

    def make_comment():
        pass

    def send_friend_request():
        pass
