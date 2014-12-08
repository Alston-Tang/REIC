__author__ = 'tang'

import pymongo
from pymongo import errors
from datetime import datetime
from bson.objectid import ObjectId
# from app import app


def _fun_var(a):
    if callable(a):
        return a()
    else:
        return a


class BaseModel:
    db = pymongo.MongoClient().reic

    def __init__(self, obj_id=None, **kwargs):
        self.attr = {}
        self.attach = False
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

    def __unicode__(self):
        rv = u""
        for item in self.attr:
            rv += u"{key}:{value}\n".format(key=unicode(item), value=unicode(self.attr[item]))
        return rv

    def __str__(self):
        return unicode(self).encode(encoding='utf-8')

    def commit(self):
        if self.attach:
            return self._update()
        else:
            return self._insert()

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

    @classmethod
    def remove(cls, query=None, del_all=False):
        if not query:
            if del_all:
                # Only when del_all set to true will translate a none query to delete all
                query = {}
            else:
                # TODO: Throw a exception
                return False
        return cls.collection.remove(query)

    def destroy(self):
        if not self.attach:
            return False
        else:
            self.remove({"_id": self.attr["_id"]})

    def _fetch(self, user_id):
        rv = self.collection.find_one({"_id": user_id})
        if rv:
            for item in self.fields_list:
                self.attr[item] = rv[item]
            return True
        else:
            return False

    def _insert(self):
        insert_id = self.attr.pop("_id", None)
        if "_id" is None:
            # Use None as _id is not allowed, a generated ObjectId will be assigned
            self.attr["_id"] = ObjectId()
        rv = self.collection.insert(self.attr)
        if rv:
            self.attach = True
        return rv

    def _update(self):
        obj_id = self.attr.pop("_id", None)
        if obj_id is None:
            # There should be a not None id for update, or a exception will be thrown
            # TODO: Throw a exception
            return False
        return self.collection.update({"_id": obj_id}, self.attr)






