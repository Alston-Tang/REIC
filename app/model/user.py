from base import BaseModel
from datetime import datetime
from hashlib import sha256


class User(BaseModel):
    fields_list = ['college', 'create_time', 'dept', 'email', 'member', 'password', 'sid', 'tel', 'username',
                   'year']
    field_default = [None, datetime.today, None, None, False, None, None, None, None, None]
    collection = BaseModel.db.users

    def __init__(self, model_id=None, **kwargs):
        BaseModel.__init__(self, model_id, **kwargs)

    @staticmethod
    def pwd_hash(password):
        return sha256(password).hexdigest()

    def valid(self):
        """
        valid function requires 'email' and 'password' field already assigned
        :return: A attached user model if exists such user that match the email and password in attr, else False
        """
        if self.attach:
            # The User is valid because this object is returned from db
            return self
        else:
            # Use email and password to query
            result = self.find({'email': self.attr['email'], 'password': self.pwd_hash(self.attr['password'])})
            if result and len(result) == 1:
                return result[0]
            else:
                return False

    @classmethod
    def exist(cls, email):
        """
        Determine whether a email is taken up by a user
        :param email: the email to be test
        :return:True if a user already use this email address as account email, False if not
        """
        result = cls.find({'email': email})
        if result:
            if len(result) > 1:
                # TODO duplicated email! Write to error log
                pass
            return True
        else:
            return False