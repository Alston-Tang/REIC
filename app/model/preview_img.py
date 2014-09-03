__author__ = 'tang'
from . import BaseModel


class PreviewImg(BaseModel):
    def __init__(self):
        BaseModel.__init__(self)
        self.collection = self.db.previewImage

    def insert(self, data, **kwargs):
        """
        :param **kwargs: not use now
        :param data: data of image in dataUri format
        :return: true for success, false for error
        """
        if not data:
            return
        return BaseModel.insert(self, self.collection, ['data'], {'data': data})

    def modify(self, img_id, data, **kwargs):
        if not data:
            return
        return BaseModel.modify(self, self.collection, {'_id': img_id}, {'data': data})

    def get_by_id(self, img_id):
        return BaseModel.get_one(self, self.collection, {'_id': img_id})

preview_img = PreviewImg()