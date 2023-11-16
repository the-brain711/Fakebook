from .enums import FriendRequestStatus
from datetime import datetime
import MySQLdb.cursors


class FriendRequest:
    def __init__(self, db=None, friend_requester_id=0, friend_accepter_id=0, friend_accepter_username="", status=FriendRequestStatus.PENDING.value, friendship_date: datetime=None):
        self.db = db
        self.cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        
        self.friend_requester_id = friend_requester_id
        self.friend_accepter_id = friend_accepter_id
        self.friend_accepter_username = friend_accepter_username
        self.status = status
        self.friendship_date = friendship_date
        pass

    def accept_friend_request(self):
        db = self.db
        cursor = self.cursor
        friendship_date = datetime.now()
        
        cursor.execute(
            "UPDATE friends_tb SET friend_request_status = 'ACCEPTED', friendship_date = %s WHERE friend_requester_id = %s AND friend_accepter_id = %s",
            (
                friendship_date,
                self.friend_requester_id,
                self.friend_accepter_id,
            ),
        )
        
        db.connection.commit()
        db.connection.close()

    def decline_friend_request(self):
        db = self.db
        cursor = self.cursor
        
        cursor.execute(
            "DELETE FROM friends_tb WHERE friend_requester_id = %s AND friend_accepter_id = %s",
            (
                self.friend_requester_id,
                self.friend_accepter_id,
            ),
        )
        
        db.connection.commit()
        db.connection.close()