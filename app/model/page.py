__author__ = 'tang'

from time import time
from . import BaseModel


class Page(BaseModel):
    """

    """
    def __init__(self):
        BaseModel.__init__(self)
        self.collection = self.db.pages

    def insert(self, **opt):
        #fake creator
        opt['creator'] = 'tang'

        from app.helper.require import require, default
        #Check exists
        require(['creator'], opt)
        default({'title': 'Untitled', 'section': []}, opt)
        #Update time
        opt['create_time'] = time()
        opt['modified_time'] = time()
        #Insert
        require=['creator', 'section', 'create_time', 'modified_time', 'title']
        BaseModel.insert(self, self.collection, require, opt)

