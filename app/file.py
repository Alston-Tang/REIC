__author__ = 'Tang'

from os import listdir
from app import root_path

upload_dir = (root_path+'/static/upload').replace('\\', '/')

class File:
    def __init__(self, name


class GetHandler:
    def __init__(self, opt):
        if dir in opt:
            self.path = upload_dir+'/'+opt[dir]
        else:
            raise NameError('No specify upload directory')

        # Check End
        self.files = []
        for file in listdir(self.path):
            self.files.append(file)

a=GetHandler({dir:'edit'})