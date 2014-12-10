from __future__ import unicode_literals

__author__ = 'tang'


from user import User
from section import Section
from page import Page
from preview_img import PreviewImg
from member import Member
from activitity import Activity
from bson import ObjectId


a = Activity.find()[0]
a.attr['venue'] = "CUHK"
a.commit()