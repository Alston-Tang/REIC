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
        if not require(['creator'], opt):
            return False
        default({'title': 'Untitled', 'section': []}, opt)
        #Update time
        opt['create_time'] = time()
        opt['modified_time'] = time()
        #Insert
        require = ['creator', 'section', 'create_time', 'modified_time', 'title']
        return BaseModel.insert(self, self.collection, require, opt)

    def get_all(self):
        return BaseModel.get(self, self.collection, {})

    def get(self, **require):
        return BaseModel.get(self, self.collection, require)

    def get_all_content(self):
        from . import Section
        section_model = Section()
        pages = self.get_all()
        for page in pages:
            page['section_detail'] = []
            for section in page['section']:
                section_result = section_model.get(_id=section)[0]
                page['section_detail'].append(section_result)

        return pages

    def get_content(self, **opt):
        from . import Section
        section_model = Section()
        pages = BaseModel.get(self, self.collection, opt)
        for page in pages:
            page['section_detail'] = []
            for section in page['section']:
                section_result = section_model.get(_id=section)[0]
                page['section_detail'].append(section_result)

        return pages


