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