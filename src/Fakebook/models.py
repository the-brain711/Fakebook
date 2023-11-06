from datetime import datetime
from enum import Enum
import MySQLdb.cursors


##### ENUMS #####
class FriendRequestStatus(Enum):
    ACCEPTED = 1
    REJECTED = 2
    PENDING = 3


##### CUSTOM DATATYPES #####
class Name:
    def __init__(self, first_name="", middle_name="", last_name=""):
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name


class Address:
    def __init__(self, street="", city="", state="", country="", zipcode=0):
        self.street = street
        self.city = city
        self.state = state
        self.country = country
        self.zipcode = zipcode


class Friend:
    def __init__(self, friend_id=0, friendship_date=""):
        self.friend_id = friend_id
        self.friendship_date = friendship_date


##### CLASSES #####
class Person:
    def __init__(self):
        self.name: Name = None
        self.address: Address = None
        self.email = ""
        self.phone = ""
        self.gender = ""
        self.date_of_birth: datetime = None
        pass


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


class FriendsList:
    def __init__(self):
        self.total_friends_count = 0
        self.friends = []
        self.friends.append(Friend())

    def add_friend():
        pass

    def remove_friend():
        pass


class FriendRequest:
    def __init__(self, user_id=0, friend_id=0):
        self.user_id = user_id
        self.friend_id = friend_id
        self.status: FriendRequestStatus = FriendRequestStatus.PENDING.value
        self.creation_date: datetime = None
        pass

    def accept_friend_request():
        pass

    def reject_friend_request():
        pass


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


class Comment:
    def __init__(self, text="", likes=0):
        self.text = text
        self.likes = likes
        self.creation_date = ""
