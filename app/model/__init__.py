__author__ = 'tang'
import sys
from bson.objectid import ObjectId
import pymongo


client = pymongo.MongoClient()
db = client.reic

class BaseModel:
    """
    Base of all model classes. Include db connection inf
    """
    def __init__(self):
        self.db = db

    @staticmethod
    def object_id_validation(object_id):
        if not isinstance(object_id, ObjectId):
            if ObjectId.is_valid(object_id):
                object_id = ObjectId(object_id)

        return object_id

    def insert(self, collection, require, data):
        """
        :param collection: collection to be inserted
        :param require: required pairs in data. if empty, all pairs will be inserted
        :param data: a dictionary contains key, content pairs
        :return: return true if success else return false
        """
        json_set = {}

        if not require:
            #list is empty
            for key in data:
                json_set[key] = data[key]
        else:
            for key in require:
                if not key in data:
                    data[key] = 'undefined'
                json_set[key] = data[key]
        try:
            return collection.insert(json_set)
        except Exception:
            print "Insert failed!"
            print(sys.exc_info()[0])
            return False

    def get(self, collection, require):
        """
        :param collection: collection to be inserted
        :param require: required document pattern in database, if empty all documents will be returned
        :return: return a list of documents
        """
        rt = []
        if not require:
            cursor = collection.find()
        else:
            #If an valid object id string given, convert to object id class
            if '_id' in require:
                require['_id'] = BaseModel.object_id_validation(require['_id'])
            cursor = collection.find(require)

        for doc in cursor:
            rt.append(doc)
        return rt

    def get_one(self, collection, require):
        """
        :param collection: collection to be inserted
        :param require: required document pattern in database, if empty all documents will be returned
        :return: return a documents self
        """
        if not require:
            cursor = collection.find_one()
        else:
            if '_id' in require:
                require['_id'] = BaseModel.object_id_validation(require['_id'])
            cursor = collection.find_one(require)
        return cursor

from section import section
from page import page
from user import user

