__author__ = 'tang'


def require(require_list,data):
    for item in require_list:
        if not item in data:
            return False
    return True


def default(default_dict,data):
    for item in default_dict:
        if not item in data:
            data[item] = default_dict[item]
    return True
