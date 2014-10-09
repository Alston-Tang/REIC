__author__ = 'Tang'

from flask import render_template, url_for, request, redirect, session
from app import app, file, model
from time import time, localtime, strftime
import json


@app.route('/')
def index():
    return render_page('index')


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
        type = request.args.get('type')
        return file.upload_test.get()
    elif request.method == 'POST':
        upload_file = request.files.get('files[]')
        return file.upload_test.post(upload_file)


@app.route('/ajax/upload/pic', methods=['GET'])
def public_pic():
    return file.upload_test.get_pic()


# file upload ajax handle delete
@app.route('/ajax/file_upload/<file_name>', methods=['DELETE'])
def main_delete(file_name):
    if not request.method == 'DELETE':
        print "Strange thing is happening"
    return file.upload_test.delete(file_name)


#log in handler
@app.route('/signIn', methods=['GET','POST'])
def signin():
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
@app.route('/signOut', methods=['GET', 'POST'])
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
@app.route('/signUp', methods=['GET', 'POST'])
def signup():
    from app.helper.form import SignUp
    from app.helper.sha256_pass import encode
    form = SignUp(request.form)
    if request.method == 'GET':
        return render_template('signup.html', form=form)
    elif request.method == 'POST':
        if form.validate():
            #Copy form data to user information dictionary
            user_inf = {}
            for key, value in request.form.items():
                user_inf[key] = value
            #Validate whether this user is member of REIC according to SID
            user_inf['member'] = model.member.valid(int(request.form['sid']))
            #SHA1 password
            user_inf['password'] = encode(user_inf['password'])
            print(user_inf)
            model.user.insert(data_=user_inf)
            return redirect(url_for('index'))
        else:
            return render_template('signup.html', form=form)


#Editor load and save handle
@app.route('/editor', methods=['GET', 'POST'])
def editor():
    if request.method == 'GET':
        section_id = request.args.get('sec', '')
        section = model.section.get_one(_id=section_id)
        if section:
            return render_template('edit.html', section=section['content'], create_time=section['create_time'],
                                   id=section_id, creator=section['creator'], modified_time=section['modified_time'])
        else:
            return render_template('edit.html', create=True, create_time=time(), id="")
    if request.method == 'POST':
        #Get upload information
        section_id = request.form.get('id', "")
        title = request.form.get('title', "")
        create_time = request.form.get('create_time', time())
        modified_time = float(request.form.get('modified_time', time()))
        content = request.form.get('content', "")
        preview_img = request.form.get('preview_img', False)
        #Check
        if content == "":
            return json.dumps({'error': 'Empty content'})
        if title == "":
            return json.dumps({'error': 'Empty title'})
        #Check end
        #If it is a new section
        if section_id == "":
            new_id = model.section.insert(title=title, create_time=create_time, modified_time=modified_time,
                                          content=content, creator='tang', preview_img=preview_img)
            if new_id:
                return json.dumps({'success': True, 'id': str(new_id)})
            else:
                return json.dumps({'error': 'Insert failed at db'})
        #else if it is a existing section
        else:
            section = model.section.get_one(_id=section_id)
            #Update Preview Image
            #If an existing image do not have a preview image
            if not 'preview_img' in section:
                #Create an preview image
                section['preview_img'] = model.preview_img.insert(preview_img)
            else:
                model.preview_img.modify(section['preview_img'], preview_img)
            rv = model.section.modify({'_id': section_id}, {'title': title, 'modified_time': modified_time,
                                                            'content': content, 'preview_img': section['preview_img']})
            if rv.get("n", False) != 1:
                return json.dumps({'error': 'Unexpected update'})
            else:
                return json.dumps(({'success': True, 'id': section_id}))


@app.route('/manage/sections', methods=['GET', 'DELETE'])
def manage_sections():
    if request.method == 'GET':
        sections = model.section.get_all_full()
        #Convert time from Unix Stamp to Python time
        for section in sections:
            section['create_time'] = strftime("%Y/%m/%d %H:%M", localtime(float(section['create_time'])))
            section['modified_time'] = strftime("%Y/%m/%d %H:%M", localtime(float(section['modified_time'])))
        return render_template("manage/section.html", sections=sections)
    if request.method == 'DELETE':
        if model.section.remove_by_id(request.form['id']):
            return json.dumps({'success': True})


@app.route('/email/generator')
def generator():
    return render_template('tools/email_generator.html')


@app.route('/test')
def test():
    if model.member.valid(1155014334):
        return "Valid"
    else:
        return "Invalid"


@app.route('/myActivities')
def my_activities():
    return render_template('myactivities.html')

#no rule matched, then treat it as a page
@app.route('/<page_title>')
def render_page(page_title):
    require_page = model.page.get_a_content(title=page_title)
    if require_page:
        return render_template('index.html', title=page_title, content=require_page, nav_bar=app.nav_bar)
    else:
        return page_not_found("")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404
