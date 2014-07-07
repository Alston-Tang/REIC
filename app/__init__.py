__author__ = 'Tang'

from flask import Flask
app = Flask(__name__)

from os import path
root_path = path.dirname(path.abspath(__file__))

from app import views