from datetime import datetime


class Comment:
    def __init__(self, comment_id: int=0, commenter_id: int=0, commenter_name: str="", text: str="", creation_date: datetime=None):
        self.comment_id = comment_id
        self.commenter_id = commenter_id
        self.commenter_name = commenter_name
        self.text = text
        self.creation_date = creation_date
