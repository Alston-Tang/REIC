from base import BaseModel
from section import Section
from datetime import datetime


class Activity(BaseModel):
    fields_list = ['disappear_time', 'name', 'appear_time', 'venue', 'time_slot', 'due_time', 'time', 'description']
    field_default = [datetime.today, "Activity", datetime.today, None, None, datetime.today, datetime.today, None]
    collection = BaseModel.db.activities

    def __init__(self, model_id=None, **kwargs):
        BaseModel.__init__(self, model_id, **kwargs)
