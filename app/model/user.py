from base import BaseModel
from datetime import datetime


class User(BaseModel):
    fields_list = ['college', 'create_time', 'dept', 'email', 'member', 'password', 'sid', 'tel', 'username',
                   'year']
    field_default = [None, datetime.today, None, None, False, None, None, None, None, None]
    collection = BaseModel.db.users

    def __init__(self, model_id=None, **kwargs):
        BaseModel.__init__(self, model_id, **kwargs)