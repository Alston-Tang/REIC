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
    fields_list = []
    field_default = []
    field_join = []
    collection = None
    auto_join = False

    def __init__(self, obj_id=None, **kwargs):
        self.attr = {}
        self.attach = False
        # Determine whether create a new empty object or fetch a existing object from DB
        if obj_id and self._fetch(obj_id):
            self._post_attached()
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
            if "_id" in kwargs:
                self.attr["_id"] = kwargs["_id"]

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

    def destroy(self):
        if not self.attach:
            return False
        else:
            return self.remove({"_id": self.attr["_id"]})

    def join(self):
        if self.field_join:
            for field in self.field_join:
                # Traverse all fields to be joined
                model_class = self.field_join[field]
                if isinstance(self.attr[field], list):
                    # This field is a []
                    self.attr[field] = self._join_list(self.attr[field], model_class)
                elif isinstance(self.attr[field], dict):
                    # This field is a {}
                    self.attr[field] = self._join_dict(self.attr[field], model_class)
                else:
                    # This field is a value
                    self.attr[field] = self._join_value(self.attr[field], model_class)

    @classmethod
    def find(cls, query=None, join=False):
        if not query:
            query = {}
        res = cls.collection.find(query)
        rv = []
        if res:
            for item in res:
                temp_model = (cls(**item))
                temp_model._post_attached()
                if join:
                    temp_model.join()
                rv.append(temp_model)
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

    @staticmethod
    def _join_dict(attr_dict, model_class):
        for item in attr_dict:
            foreign_model = model_class(attr_dict[item])
            if not foreign_model.attach:
                # TODO Throw a exception
                pass
            attr_dict[item] = foreign_model.attr
        return attr_dict

    @staticmethod
    def _join_list(attr_list, model_class):
        rv = []
        for item in attr_list:
            foreign_model = model_class(item)
            if not foreign_model.attach:
                # TODO Throw a exception
                pass
            rv.append(foreign_model.attr)
        return rv

    @staticmethod
    def _join_value(attr_value, model_class):
        foreign_model = model_class(attr_value)
        if not foreign_model.attach:
                # TODO Throw a exception
                pass
        return foreign_model.attr

    def _fetch(self, user_id):
        rv = self.collection.find_one({"_id": user_id})
        if rv:
            for item in self.fields_list:
                self.attr[item] = rv[item]
            self.attr["_id"] = rv["_id"]
            return True
        else:
            return False

    def _post_attached(self):
        self.attach = True
        if self.auto_join:
            self.join()

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