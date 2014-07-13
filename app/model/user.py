__author__ = 'tang'

from time import time
from . import BaseModel


class User(BaseModel):
    def __init__(self):
        BaseModel.__init__(self)
        self.collection=self.db.users

    def insert(self, **opt):
        if opt['data']:
            opt = opt['data']

        from app.helper.require import require, default
        require(['username', 'password','email'],opt)
        default({'tel': False, 'dept': False, 'sid': False, 'year': False, 'extra': []}, opt)
        opt['activity'] = []
        opt['inf'] = []
        opt['create_time']=time()
        require = ['username', 'password', 'email', 'create_time', 'tel', 'dept', 'sid', 'year', 'extra', 'activity', 'inf']
        BaseModel.insert(self,self.collection,require,opt)