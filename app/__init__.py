__author__ = 'Tang'

from flask import Flask
app = Flask(__name__)

from os import path
root_path = path.dirname(path.abspath(__file__))
print 'root path is: '+root_path

from app import views