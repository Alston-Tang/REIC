from base import BaseModel
from preview_img import PreviewImg
from datetime import datetime


class Section(BaseModel):
    fields_list = ['content', 'create_time', 'creator', 'modified_time', 'preview_img', 'title']
    field_default = [None, datetime.today, None, datetime.today(), None, "Untitled"]
    field_join = {"preview_img": PreviewImg}
    collection = BaseModel.db.sections

    def __init__(self, model_id=None, **kwargs):
        BaseModel.__init__(self, model_id, **kwargs)