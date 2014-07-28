__author__ = 'tang'

from time import time
from . import BaseModel


class User(BaseModel):
    def __init__(self):
        BaseModel.__init__(self)
        self.collection = self.db.users

    def insert(self, **opt):
        if opt['data_']:
            for item in opt['data_']:
                opt[item] = opt['data_'][item]

        from app.helper.require import require, default
        if not require(['username', 'password','email'], opt):
            return False
        default({'tel': False, 'dept': False, 'sid': False, 'year': False, 'extra': []}, opt)
        opt['activity'] = []
        opt['inf'] = []
        opt['create_time']=time()
        require = ['username', 'password', 'email', 'create_time', 'tel', 'dept', 'sid', 'year', 'extra', 'activity', 'inf']
        return BaseModel.insert(self,self.collection, require, opt)

    def get(self, **require):
        return BaseModel.get(self, self.collection, require)

    def valid(self, **opt):

        from app.helper.require import require
        from app.helper import sha256_pass

        if not require(['email','password'], opt):
            return False
        opt['password'] = sha256_pass.encode(opt['password'])
        cur_user = BaseModel.get(self, self.collection, opt)
        if not cur_user:
            return False
        else:
            return cur_user[0]

#Global Model Instance
user = User()