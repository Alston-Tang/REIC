__author__ = 'tang'

from time import time
from . import BaseModel
from preview_img import preview_img


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
        if not require(['creator'], opt):
            return False
        default({'content': "", 'title': "Untitled", 'preview_img': False}, opt)

        opt['create_time'] = time()
        opt['modified_time'] = time()

        require = ['creator', 'content', 'create_time', 'modified_time', 'title', 'preview_img']
        opt['preview_img'] = preview_img.insert(opt['preview_img'])
        return BaseModel.insert(self, self.collection, require, opt)

    def get_all(self):
        return BaseModel.get(self, self.collection, {})

    def get(self, **require):
        return BaseModel.get(self, self.collection, require)

    def get_one(self, **require):
        return BaseModel.get_one(self, self.collection, require)

    def modify(self, spec, document, **kwargs):
        return BaseModel.modify(self, self.collection, spec, document)

    def get_one_full(self, **require):
        res = self.get_one(**require)
        #Join preview image
        res['preview_img'] = preview_img.get_by_id(res['preview_img'])
        return res

    def get_all_full(self):
        res = BaseModel.get(self, self.collection, {})
        for each_section in res:
            if 'preview_img' in each_section:
                each_section['preview_img'] = preview_img.get_by_id(each_section['preview_img'])['data']
            else:
                each_section['preview_img'] = ""
        return res

    def remove_by_id(self, sec_id):
        res = BaseModel.remove(self, self.collection, {'_id': sec_id})
        if not res['err']:
            return True
        else:
            return False



#Global Model Instance
section = Section()