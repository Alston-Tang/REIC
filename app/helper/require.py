__author__ = 'tang'
import datetime


def require(require_list, data):
    for item in require_list:
        if not item in data:
            return False
    return True


def default(default_dict, data):
    for item in default_dict:
        if not item in data:
            data[item] = default_dict[item]
    return True


def is_datetime(field_list, data):
    for item in field_list:
        if item in data:
            return isinstance(data[item], datetime.datetime)
    else:
        return False


def map_time_slot(time_slot):
    rv = []
    for time in time_slot:
        rv.append((time, 0))
    return rv