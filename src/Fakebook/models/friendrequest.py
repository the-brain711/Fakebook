from .enums import FriendRequestStatus
from datetime import datetime


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