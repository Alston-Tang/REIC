__author__ = 'tang'


def decompose_user(user_model):
    """
    Transfer a user model instance to a dictionary
    :param user_model: the user model to be decomposed
    :return: a {}
    """
    return {'_id': str(user_model.attr['_id']), "username": user_model.attr['username']}
