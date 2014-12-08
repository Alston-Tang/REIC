from base import BaseModel
from datetime import datetime


class Page(BaseModel):
    fields_list = ['create_time', 'creator', 'modified_time', 'section', 'title']
    field_default = [datetime.today, None, datetime.today(), [], "Untitled"]
    collection = BaseModel.db.pages

    def __init__(self, user_id=None, **kwargs):
        BaseModel.__init__(self, user_id, **kwargs)