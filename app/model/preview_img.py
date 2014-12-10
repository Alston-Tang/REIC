from base import BaseModel
from section import Section
from datetime import datetime


class PreviewImg(BaseModel):
    fields_list = ['data']
    field_default = [None]
    collection = BaseModel.db.previewImage

    def __init__(self, model_id=None, **kwargs):
        BaseModel.__init__(self, model_id, **kwargs)