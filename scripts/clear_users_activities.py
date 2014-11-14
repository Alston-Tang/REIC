__author__ = 'tang'

from app.model import user, activity, BaseModel
import pymongo

collection = pymongo.MongoClient().reic.users

rv = collection.update({}, {"$unset": {"activity": 1}})
print(rv)
rv = collection.update({}, {"$set": {"activity": {}}})
print(rv)