from .datatypes import Name, Address
from .person import Person
from .timeline import Timeline
from .friendslist import FriendsList
from .friendrequest import FriendRequest
from .enums import FriendRequestErrors
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
        self.__get_user_data()

        self.timeline = Timeline(db, user_id)
        self.friends_list = FriendsList(db, user_id)
        self.friend_requests = self.__get_friend_requests()

    def __get_user_data(self):
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

    def __get_friend_requests(self):
        cursor = self.cursor
        cursor.execute(
            "SELECT users_tb.username, friends_tb.friend_requester_id, friends_tb.friend_accepter_id, friends_tb.friendship_date FROM friends_tb INNER JOIN users_tb ON friends_tb.friend_requester_id = users_tb.id WHERE friends_tb.friend_accepter_id = %s AND friends_tb.friend_request_status = 'PENDING' ORDER BY friendship_date DESC",
            (self.user_id,),
        )
        friend_requests = cursor.fetchall()

        if friend_requests:
            items = dict()
            for fr in friend_requests:
                item = FriendRequest(
                    db=self.db,
                    friend_requester_id=fr["friend_requester_id"],
                    friend_accepter_id=fr["friend_accepter_id"],
                    friend_accepter_username=fr["username"],
                    friendship_date=fr["friendship_date"],
                )
                items[fr["friend_requester_id"]] = item

            return items
        else:
            return None

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

        ## Get post id from newly created post
        # cursor.execute("SELECT LAST_INSERT_ID()")
        # post_id = cursor.fetchone()

        ## Create table to check whether user has liked a post or not. Default is not liked.
        # cursor.execute(
        #    "INSERT INTO liked_posts_tb (liked_post_id, liked_user_id) VALUES(%s, %s)",
        #    (
        #        post_id,
        #        self.user_id,
        #    ),
        # )

        db.connection.commit()
        db.connection.close()

    def like_post(self, post_id: int):
        db = self.db
        cursor = self.cursor

        cursor.execute(
            "SELECT * FROM liked_posts_tb WHERE liked_post_id = %s AND liked_user_id = %s AND liked_status = 1",
            (
                post_id,
                self.user_id,
            ),
        )
        
        already_liked = cursor.fetchone()
        if not already_liked:
            cursor.execute(
                "INSERT INTO liked_posts_tb (liked_post_id, liked_user_id) SELECT post_id, user_id FROM posts_tb WHERE post_id = %s AND user_id = %s;",
                (
                    post_id,
                    self.user_id,
                ),
            )
            
            cursor.execute(
                "UPDATE posts_tb SET likes = likes + 1 WHERE post_id = %s",
                (post_id,),
            )

        # cursor.execute(
        #    "UPDATE posts_tb INNER JOIN liked_posts_tb ON posts_tb.post_id = liked_posts_tb.liked_post_id SET posts_tb.likes = posts_tb.likes + 1, liked_posts_tb.liked_status = 1 WHERE posts_tb.post_id = %s AND liked_posts_tb.liked_status = 0",
        #    (post_id,),
        # )

        db.connection.commit()
        db.connection.close()
        
    def search_for_user(self, username: str):
        db = self.db
        cursor = db.connection.cursor()
        
        # Get friend's user id
        cursor.execute(
            "SELECT * FROM users_tb WHERE username = %s",
            (username,),
        )
        user = cursor.fetchone()
        
        db.connection.commit()
        db.connection.close()
        
        if user:
            return user
        else:
            return None
        
    def send_friend_request(self, friend_username: str):
        db = self.db
        cursor = db.connection.cursor()
        friendship_date = datetime.now()

        # Get friend's user id
        cursor.execute(
            "SELECT id FROM users_tb WHERE username = %s",
            (friend_username,),
        )
        friend_id = cursor.fetchone()
        if friend_id == None:
            return FriendRequestErrors.INVALID_USER
        else:
            friend_id = friend_id[0]

        # Check for existing friend request
        cursor.execute(
            "SELECT CASE WHEN EXISTS (SELECT * FROM friends_tb WHERE friend_requester_id = %s AND friend_accepter_id = %s) THEN TRUE ELSE FALSE END AS BOOL",
            (
                self.user_id,
                friend_id,
            ),
        )
        does_friend_request_exist = cursor.fetchone()[0]
        if does_friend_request_exist == True:
            return FriendRequestErrors.FRIEND_REQUEST_ALREADY_EXISTS

        # Send friend request to friend
        cursor.execute(
            "INSERT INTO friends_tb (friend_requester_id, friend_accepter_id, friendship_date) VALUES (%s, %s, %s)",
            (
                self.user_id,
                friend_id,
                friendship_date,
            ),
        )

        db.connection.commit()
        db.connection.close()

    def make_comment(self, post_id: int, comment_text: str):
        db = self.db
        cursor = self.cursor
        creation_date = datetime.now()

        cursor.execute(
            "INSERT INTO comments_tb (commenter_id, post_id, comment, creation_date) VALUES(%s, %s, %s, %s)",
            (
                self.user_id,
                post_id,
                comment_text,
                creation_date,
            ),
        )

        db.connection.commit()
        db.connection.close()

    def reply_to_comment(self, post_id: int, comment_id: int, reply_text: str):
        db = self.db
        cursor = self.cursor
        creation_date = datetime.now()

        cursor.execute(
            "INSERT INTO comments_tb (commenter_id, post_id, comment, creation_date, comment_replied_to) VALUES(%s, %s, %s, %s, %s)",
            (
                self.user_id,
                post_id,
                reply_text,
                creation_date,
                comment_id,
            ),
        )

        db.connection.commit()
        db.connection.close()
