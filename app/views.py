__author__ = 'Tang'

from flask import render_template, url_for, request, redirect, session
from app import app, file, model

@app.route('/')
def index():
    page = model.page.get_content(title='index')[0]
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
@app.route('/ajax/file_upload', methods=['GET', 'POST'])
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
@app.route('/signin',methods=['GET','POST'])
def sign_in():
    from app.helper.form import SignIn
    form = SignIn()
    if request.method == 'GET':
        return render_template("signin.html", title='Sign In', nav_bar=app.nav_bar, form=form)
    if request.method == 'POST':
        cur_user = model.user.valid(email=request.form['email'], password=request.form['password'])
        if cur_user:
            session['username'] = cur_user['username']
            session['user_id'] = str(cur_user['_id'])
            return redirect(url_for('index'))
        else:
            return render_template("signin.html", title='Sign In', nav_bar=app.nav_bar, form=form, error="Invalid Username or Password")
#log out handler
@app.route('/signout', methods=['GET', 'POST'])
def sign_out():
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/setting')
def setting():
    from bson.objectid import ObjectId
    if 'user_id' in session:
        uid = ObjectId(oid=session['user_id'])
        cur_user = model.user.get(_id=uid)[0]
        return render_template("setting.html", cur_user=cur_user)
    else:
        return render_template("signin.html", title='Sign In', nav_bar=app.nav_bar, error="Invalid username of password")

#signup handler
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    from app.helper.form import SignUp
    form = SignUp(request.form)
    if request.method == 'GET':
        return render_template('signup.html', form=form)
    elif request.method == 'POST':
        if form.validate():
            model.user.insert(data_=request.form)
            return redirect(url_for('index'))
        else:
            return render_template('signup.html', form=form)

#Below is for test
@app.route('/test')
def test():
    from app.helper.form import SignUp
    form = SignUp(request.form)
    return render_template('test.html',form=form)