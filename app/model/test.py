from __future__ import unicode_literals

__author__ = 'tang'


from user import User
from section import Section
from page import Page

sections = Page.find()
for sec in sections:
    print(sec)
