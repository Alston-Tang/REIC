__author__ = 'tang'

from time import time
from . import BaseModel

class Section(BaseModel):
    """
___
    """
    def __init__(self):
        BaseModel.__init__(self)
        self.collection = self.db.sections

    def insert(self, **opt):
        #fake creator
        opt['creator'] = 'tang'

        from app.helper.require import require, default
        require(['creator'], opt)
        default({'content': "", 'title': "Untitled"}, opt)

        opt['create_time'] = time()
        opt['modified_time'] = time()

        require = ['creator', 'content', 'create_time', 'modified_time', 'title']
        BaseModel.insert(self, self.collection, require, opt)

    def get_all(self):
        return BaseModel.get(self, self.collection, {})

    def get(self, **require):
        return BaseModel.get(self, self.collection, require)