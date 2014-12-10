from base import BaseModel
from section import Section


class Member(BaseModel):
    fields_list = ['major', 'college', 'firstname', 'sid', 'lastname', 'year', 'email', 'tel']
    field_default = [None, None, None, None, None, None, None, None]
    collection = BaseModel.db.regMembers

    def __init__(self, model_id=None, **kwargs):
        BaseModel.__init__(self, model_id, **kwargs)