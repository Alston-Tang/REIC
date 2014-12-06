__author__ = 'tang'

import pymongo
from pymongo import errors
from datetime import datetime
from bson.objectid import ObjectId
from app import app


def _fun_var(a):
    if callable(a):
        return a()
    else:
        return a


class BaseModel:
    attach = False
    attr = {}
    collection = None
    db = pymongo.MongoClient().test

    def __init__(self, obj_id=None, **kwargs):
        for item in self.fields_list:
            self.attr[item] = None
        # Determine whether create a new empty object or fetch a existing object from DB
        if obj_id and self._fetch(obj_id):
            self.attach = True
        else:
            attach = False
            # Set attributes to key-value pair from kwargs, if not found then set to default
            count = 0
            for item in self.fields_list:
                if item in kwargs:
                    self.attr[item] = kwargs[item]
                else:
                    self.attr[item] = _fun_var(self.field_default[count])
                count += 1

    def __str__(self):
        rv = ""
        for item in self.attr:
            rv += "{key}:{value}\n".format(key=str(item), value=str(self.attr[item]))
        return rv

    def commit(self):
        if self.attach:
            self._update()
        else:
            self._insert()

    @classmethod
    def find(cls, query=None):
        if not query:
            query = {}
        res = cls.collection.find(query)
        rv = []
        if res:
            for item in res:
                rv.append(cls(**item))

        return rv

    def _fetch(self, user_id):
        rv = self.collection.find_one({"_id": user_id})
        if rv:
            for item in self.fields_list:
                self.attr[item] = rv[item]
            return True
        else:
            return False

    def _insert(self):
        if "_id" in self.attr and self.attr["_id"] is None:
            # Use None as _id is not allowed
            del self.attr["_id"]
        return self.collection.insert(self.attr)

    def _update(self):
        obj_id = self.attr.pop("_id", None)
        if obj_id is None:
            # There should be a not None id for update, or a exception will be thrown
            # TODO: Throw a exception
            return False
        return self.collection.update({"_id": obj_id}, self.attr)


class User(BaseModel):
    fields_list = ['_id', 'college', 'create_time', 'dept', 'email', 'member', 'password', 'sid', 'tel', 'username',
                   'year']
    field_default = [None, None, datetime.today, None, None, False, None, None, None, None, None]
    collection = BaseModel.db.users

    def __init__(self, user_id=None, **kwargs):
        BaseModel.__init__(self, user_id, **kwargs)





