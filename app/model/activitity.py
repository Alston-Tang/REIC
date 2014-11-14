__author__ = 'tang'

from time import time
from . import BaseModel


class Activity(BaseModel):
    def __init__(self):
        BaseModel.__init__(self)
        self.collection = self.db.activities

    def insert(self, **opt):
        from app.helper.require import require, default, is_datetime, map_time_slot
        #Check whether field exists
        if not require(['name', 'time', 'start_time', 'due_time', 'disappear_time'], opt):
            return False
        #Check whether field format is right
        if not is_datetime(['time', 'start_time', 'due_time', 'disappear_time'], opt):
            return False
        #Set default value
        default({'venue': 'TBA', 'description': 'No description yet'}, opt)
        #Init time slot, if not exists, set to False, else set to time: number of registration pair
        opt['time_slot'] = False
        opt['time_slot2'] = False
        opt['time_slot3'] = False
        if 'time_slot' in opt:
            opt['time_slot'] = map_time_slot(opt['time_slot'])
        if 'time_slot2' in opt:
            opt['time_slot2'] = map_time_slot(opt['time_slot2'])
        if 'time_slot3' in opt:
            opt['time_slot3'] = map_time_slot(opt['time_slot3'])

        #Set _id the same as name !!Duplicated name is not allowed
        opt['_id'] = opt['name']
        require = ['name', 'time', 'start_time', 'due_time', 'disappear_time', 'venue', 'description', '_id',
                   'time_slot', 'time_slot2', 'time_slot3']
        print opt
        return BaseModel.insert(self, self.collection, require, opt)

    def get(self, **require):
        return BaseModel.get(self, self.collection, require)

    def get_one(self, **require):
        return BaseModel.get_one(self, self.collection, require)
# Global Model Instance
activity = Activity()