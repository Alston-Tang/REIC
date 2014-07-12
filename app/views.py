__author__ = 'Tang'

from flask import render_template, url_for, request
from app import app, file, model

@app.route('/')
def index():
    pages = model.Page().get_all_content()
    content = ''
    nav_bar={}
    for page in pages:
        nav_bar[page['title']]=[]
        for section in page['section_detail']:
            nav_bar[page['title']].append(section['title'])
            if page['title'] == 'index':
                content += section['content']

    return render_template("index.html", content=content, title='index', nav_bar=nav_bar)


@app.route('/edit')
def edit():
    return render_template('edit.html')


@app.route('/upload')
def upload():
    return app.send_static_file('html/file_upload.html')


@app.route('/ajax/file_upload',methods=['GET', 'POST'])
def main_upload():
    if request.method == 'GET':
        return file.upload_test.get()
    elif request.method == 'POST':
        upload_file = request.files.get('files[]')
        return file.upload_test.post(upload_file)

@app.route('/ajax/file_upload/<file_name>', methods=['DELETE'])
def main_delete(file_name):
    if not request.method == 'DELETE':
        print "Strange thing is happening"
    return file.upload_test.delete(file_name)