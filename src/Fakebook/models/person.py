from .datatypes import Name, Address
from datetime import datetime


class Person:
    def __init__(self):
        self.name: Name = None
        self.address: Address = None
        self.email = ""
        self.phone = ""
        self.gender = ""
        self.date_of_birth: datetime = None
        pass