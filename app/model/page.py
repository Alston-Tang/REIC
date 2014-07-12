__author__ = 'tang'

from time import time
from . import db

class Page:
    """

    """
    def __init__(self):
        self.collection = db.pages

    def insert(self, **opt):

        #fake creator
        opt['creator']='tang'

        if not 'creator' in opt:
            print('Error:Creator not defined when insert new page')
        creator = opt['creator']
        create_time = time()
        modified_time = time()
        title = 'Untitled' if not opt['title'] else opt['title']
        section=[]
        self.collection.insert({'creator': creator,
                                'create_time': create_time,
                                'modified_time': modified_time,
                                'title': title,
                                'section': []})

