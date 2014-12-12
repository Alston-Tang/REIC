__author__ = 'Tang'
reload(__import__('sys')).setdefaultencoding('utf-8')
from flask import Flask

import pymongo

app = Flask(__name__)

from os import path, environ
root_path = path.dirname(path.abspath(__file__))

# initialize global content
# set secret key
app.secret_key = '8f1hj{%~x|#JjjU7aQ:q'
# Set upload file
app.config['UPLOAD_FOLDER'] = '/static/upload'
# Set database reference from pymongo
app.config['DB'] = pymongo.MongoClient().reic
# initialize nav_bar titles

import nav_bar
app.nav_bar = nav_bar.nav_bar_structure()
# configure log
if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler(path.join(environ['HOME'], "web_log.log"), maxBytes=10485760)
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)

# Loading global plugin
import global_plugin
from app import views