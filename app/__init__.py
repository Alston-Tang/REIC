__author__ = 'Tang'
reload(__import__('sys')).setdefaultencoding('utf-8')
from flask import Flask

app = Flask(__name__)

from os import path
root_path = path.dirname(path.abspath(__file__))

#initialize global content
#set secret key
app.secret_key = '8f1hj{%~x|#JjjU7aQ:q'
#Set upload file
app.config['UPLOAD_FOLDER'] = '/static/upload'
#initialize nav_bar titles
import nav_bar
app.nav_bar = nav_bar.nav_bar_structure()

from app import views