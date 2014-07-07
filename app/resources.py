__author__ = 'Tang'
from flask import url_for


def css(file_name):
    return url_for('get_css', css_file=file_name)


def js(file_name):
    return 0

