__author__ = 'tang'

from time import time
from . import BaseModel
from section import section


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
        pages = self.get_all()
        for page_ite in pages:
            page_ite['section_detail'] = []
            for section_ite in page_ite['section']:
                section_result = section.get(_id=section_ite)[0]
                page_ite['section_detail'].append(section_result)

        return pages

    def get_content(self, **opt):
        pages = BaseModel.get(self, self.collection, opt)
        for page_ite in pages:
            page_ite['section_detail'] = []
            for section_ite in page_ite['section']:
                section_result = section.get(_id=section_ite)[0]
                page_ite['section_detail'].append(section_result)

        return pages

#Global Model Instance
page = Page()


