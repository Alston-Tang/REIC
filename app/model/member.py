__author__ = 'tang'

from . import BaseModel


class Member(BaseModel):
    def __init__(self):
        BaseModel.__init__(self)
        self.collection = self.db.regMembers

    def valid(self, sid):
        rv = BaseModel.get_one(self, self.collection, {'sid': sid})
        return bool(rv)

#Global Model Instance
member = Member()