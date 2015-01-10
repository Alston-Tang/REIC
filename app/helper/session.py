__author__ = 'tang'


def decompose_user(user_model):
    """
    Transfer a user model instance to a dictionary
    :param user_model: the user model to be decomposed
    :return: a {}
    """
    return {'_id': str(user_model.attr['_id']), "username": user_model.attr['username']}


def admin_session(session):
    from app.model import User
    from bson import ObjectId
    if 'user' in session:
        user_id = session['user']['_id']
        return User(ObjectId(user_id)).is_admin()
    return False
