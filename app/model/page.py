from base import BaseModel
from section import Section
from datetime import datetime


class Page(BaseModel):
    fields_list = ['create_time', 'creator', 'modified_time', 'section', 'title']
    field_default = [datetime.today, None, datetime.today(), [], "Untitled"]
    field_join = {"section": Section}
    collection = BaseModel.db.pages

    def __init__(self, model_id=None, **kwargs):
        BaseModel.__init__(self, model_id, **kwargs)