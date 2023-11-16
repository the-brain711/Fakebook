from .enums import FriendRequestStatus
from datetime import datetime


class FriendRequest:
    def __init__(self, friend_accepter_id=0, friend_accepter_username="", status=FriendRequestStatus.PENDING.value, friendship_date: datetime=None):
        self.friend_accepter_id = friend_accepter_id
        self.friend_accepter_username = friend_accepter_username
        self.status = status
        self.friendship_date = friendship_date
        pass

    def accept_friend_request():
        pass

    def reject_friend_request():
        pass