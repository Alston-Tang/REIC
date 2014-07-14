__author__ = 'Tang'

from flask import render_template, url_for, request, redirect, session
from app import app, file, model

@app.route('/')
def index():
    page = model.Page().get_content(title='index')[0]
    content = ''
    for section in page['section_detail']:
        content += section['content']
    return render_template("index.html", content=content, title='index', nav_bar=app.nav_bar)


@app.route('/edit')
def edit():
    return render_template('edit.html')

# file upload static page
@app.route('/upload')
def upload():
    return app.send_static_file('html/file_upload.html')

# file upload ajax handle get & post
@app.route('/ajax/file_upload',methods=['GET', 'POST'])
def main_upload():
    if request.method == 'GET':
        return file.upload_test.get()
    elif request.method == 'POST':
        upload_file = request.files.get('files[]')
        return file.upload_test.post(upload_file)
# file upload ajax handle delete
@app.route('/ajax/file_upload/<file_name>', methods=['DELETE'])
def main_delete(file_name):
    if not request.method == 'DELETE':
        print "Strange thing is happening"
    return file.upload_test.delete(file_name)

#log in handler
@app.route('/signin',methods=['GET'])
def sign_in():
    return render_template("signin.html", title='Sign In', nav_bar=app.nav_bar)

#log out handler
@app.route('/signout', methods=['GET','POST'])
def sign_out():
    session.pop('username', None)
    return redirect(url_for('index'))

#user authentication
@app.route('/auth', methods=['POST'])
def authentication():
    user = model.User()
    username = user.valid(email=request.form['email'], password=request.form['password'])
    if username:
        session['username'] = username
        return redirect(url_for('index'))
    else:
        return render_template("signin.html", title='Sign In', nav_bar=app.nav_bar, error="Invalid username of password")