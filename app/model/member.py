from base import BaseModel
from section import Section


class Member(BaseModel):
    fields_list = ['major', 'college', 'firstname', 'sid', 'lastname', 'year', 'email', 'tel']
    field_default = [None, None, None, None, None, None, None, None]
    collection = BaseModel.db.regMembers

    def __init__(self, model_id=None, **kwargs):
        BaseModel.__init__(self, model_id, **kwargs)

    def exist(self):
        """
        exist function requires  'sid' field already assigned
        :return: A attached member model if exists such member that match the sid in attr, else False
        """
        result = self.find({"sid": self.attr['sid']})
        if self.attach:
            return True
        if result:
            if len(result) > 1:
                # TODO Write a warning to log
                pass
            return True
        else:
            return False