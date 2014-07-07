__author__ = 'Tang'

from flask import render_template, url_for
from app import app, resources


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/edit')
def edit():
    return render_template('edit.html')


@app.route('/test')
def test():
    return render_template("test.html")


@app.route('/ajax/<service_name>')
def ajax_service(service_name):
    if service_name == 'file_upload':
        return '0'
    else:
        return ""