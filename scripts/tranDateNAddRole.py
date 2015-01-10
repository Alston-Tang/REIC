# Add roll field and convert create time to ISO date

__author__ = 'tang'


import os, sys
from datetime import datetime


model_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(model_path)

from app.model import User, Section, Page

users = User.find()
for user in users:
    user.attr['roll'] = []
    if not isinstance(user.attr['create_time'], datetime):
        user.attr['create_time'] = datetime.fromtimestamp(user.attr['create_time'])
    user.commit()

pages = Page.find()
for page in pages:
    if not isinstance(page.attr['create_time'], datetime):
        page.attr['create_time'] = datetime.fromtimestamp(page.attr['create_time'])
    if not isinstance(page.attr['modified_time'], datetime):
        page.attr['modified_time'] = datetime.fromtimestamp(page.attr['modified_time'])

sections = Section.find()
for section in sections:
    if not isinstance(section.attr['create_time'], datetime):
        section.attr['create_time'] = datetime.fromtimestamp(section.attr['create_time'])
    if not isinstance(section.attr['modified_time'], datetime):
        section.attr['modified_time'] = datetime.fromtimestamp(section.attr['modified_time'])