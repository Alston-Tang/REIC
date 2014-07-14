__author__ = 'Tang'

from flask import Flask
app = Flask(__name__)

from os import path
root_path = path.dirname(path.abspath(__file__))

#initialize global content
#set secret key
app.secret_key = '8f1hj{%~x|#JjjU7aQ:q'
#initialize nav_bar titles
import nav_bar
app.nav_bar = nav_bar.nav_bar_structure()

from app import views