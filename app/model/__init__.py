__author__ = 'tang'
import pymongo
import sys

client = pymongo.MongoClient()
db = client.reic

class BaseModel:
    """
    Base of all model classes. Include db connection inf
    """
    def __init__(self):
        self.db = db

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
            collection.insert(json_set)
        except Exception:
            print "Insert failed!"
            print(sys.exc_info()[0])
            return False

        return True

    def get(self, collection, require):
        """
        :param collection: collection to be inserted
        :param require: required document pattern in database, if empty all documents will be returned
        :return: return a list of documents
        """
        rt = []
        if not require:
            cursor=collection.find()
        else:
            cursor = collection.find(require)
        for doc in cursor:
            rt.append(doc)
        return rt

from page import Page
from section import Section
from user import User

