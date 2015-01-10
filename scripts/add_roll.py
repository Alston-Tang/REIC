# Add roll field and convert create time to ISO date

__author__ = 'tang'


import os
from datetime import datetime


model_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ['PATH'] += model_path

from app.model import User

users = User.find()
for user in users:
    user.attr['roll'] = []
    user.attr['create_time'] = datetime.fromtimestamp(user.attr['create_time'])
    user.commit()