from datetime import datetime


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
    def __init__(self, friend_id: int=0, friend_fullname: str="", friend_username: str="", friendship_date: datetime=None):
        self.friend_id = friend_id
        self.friend_fullname = friend_fullname
        self.friend_username = friend_username
        self.friendship_date = friendship_date