from enum import Enum


class FriendRequestStatus(Enum):
    ACCEPTED = 1
    REJECTED = 2
    PENDING = 3

class FriendRequestErrors(Enum):
    INVALID_USER = 1
    FRIEND_REQUEST_ALREADY_EXISTS = 2
