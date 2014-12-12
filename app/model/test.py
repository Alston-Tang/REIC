from user import User
from member import Member
from section import Section
from datetime import datetime
from time import localtime

sections = Section.find()
for section in sections:
    section.attr['create_time'] = datetime.fromtimestamp(section.attr['create_time'])
    section.attr['modified_time'] = datetime.fromtimestamp(section.attr['modified_time'])
    section.commit()