from base import BaseModel
from datetime import datetime


class User(BaseModel):
    fields_list = ['_id', 'college', 'create_time', 'dept', 'email', 'member', 'password', 'sid', 'tel', 'username',
                   'year']
    field_default = [None, None, datetime.today, None, None, False, None, None, None, None, None]
    collection = BaseModel.db.users

    def __init__(self, user_id=None, **kwargs):
        BaseModel.__init__(self, user_id, **kwargs)