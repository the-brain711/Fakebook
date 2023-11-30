from .datatypes import Friend
import MySQLdb.cursors


class FriendsList:
    def __init__(self, db, user_id: int):
        self.db = db
        self.cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

        self.user_id = user_id
        self.total_friends_count = 0
        self.friends = self.__get_friends()

    def __get_friends(self):
        cursor = self.cursor
        cursor.execute(
            "SELECT users_tb.username, friends_tb.friend_accepter_id, friends_tb.friendship_date FROM friends_tb INNER JOIN users_tb ON friends_tb.friend_accepter_id = users_tb.id WHERE friends_tb.friend_requester_id = %s AND friends_tb.friend_request_status = 'ACCEPTED' UNION SELECT users_tb.username, friends_tb.friend_accepter_id, friends_tb.friendship_date FROM friends_tb INNER JOIN users_tb ON friends_tb.friend_requester_id = users_tb.id WHERE friends_tb.friend_accepter_id = %s AND friends_tb.friend_request_status = 'ACCEPTED'",
            (
                self.user_id,
                self.user_id,
            ),
        )
        friends = cursor.fetchall()

        if friends:
            self.total_friends_count = len(friends)
            friends_dict = dict()

            for friend in friends:
                item = Friend(
                    friend_id=friend["friend_accepter_id"],
                    friend_name=friend["username"],
                    friendship_date=friend["friendship_date"],
                )
                friends_dict[friend["friend_accepter_id"]] = item

            return friends_dict
        else:
            return None

    def add_friend():
        pass

    def remove_friend():
        pass
