# coding=utf-8
__author__ = 'Tang'

from flask import render_template, url_for, request, redirect, session
from app import app, file, model
from time import time, localtime, strftime
from werkzeug import secure_filename
import datetime
import json
import os


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


# log in handler
@app.route('/signIn', methods=['GET', 'POST'])
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
            return render_template("signin.html", title='Sign In', nav_bar=app.nav_bar, form=form,
                                   error="Invalid Username or Password")


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
        return render_template("signin.html", title='Sign In', nav_bar=app.nav_bar,
                               error="Invalid username of password")


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
            rv = model.user.insert(data_=user_inf)
            if not rv:
                #Come to here when insert is failed due to db error
                return render_template('error/unexpected_error.html')
            session['username'] = user_inf['username']
            session['user_id'] = str(rv)
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

@app.route('/manage/activities', methods=['GET', 'POST'])
def manage_activities():
    if request.method == 'GET':
        return render_template('manage/activity.html')
    if request.method == 'POST':
        pass


@app.route('/email/generator')
def generator():
    return render_template('tools/email_generator.html')


@app.route('/test')
def test():
    from datetime import datetime
    time_slot = []
    for hour in range(9, 12):
        time_slot.append(datetime(2014, 11, 29, hour, 0))
        time_slot.append(datetime(2014, 11, 30, hour, 30))
    for hour in range(13, 17):
        time_slot.append(datetime(2014, 11, 29, hour, 0))
        time_slot.append(datetime(2014, 11, 30, hour, 30))
    time_slot.append(datetime(2014, 11, 29, 17))
    for hour in range(9, 12):
        time_slot.append(datetime(2014, 11, 29, hour, 0))
        time_slot.append(datetime(2014, 11, 30, hour, 30))
    for hour in range(13, 17):
        time_slot.append(datetime(2014, 11, 29, hour, 0))
        time_slot.append(datetime(2014, 11, 30, hour, 30))
    time_slot.append(datetime(2014, 11, 30, 17))

    model.activity.insert(name='2014 Research Project with CBRE',
                          time=datetime(2014, 11, 20, 23, 59),
                          due_time=datetime(2014, 11, 20, 23, 59),
                          start_time=datetime(2014, 12, 1),
                          disappear_time=datetime(2015, 3, 1),
                          venue='N/A',
                          description='''The broad topic this year is “Investment behaviors of Chinese Investors in Spanish Real Estate Market”, focusing on initial drivers for different investment activities of Chinese investors. With the whole team, you are going to narrow the topic, settle the guideline, do the research and finish the report. Yes, it’s your tailor-made research project! There’ll be sub-groups focusing on different perspectives of the topic. Communicating and collaborating inside or among groups, you will definitely improve your leadership and interpersonal skills.''',
                          time_slot=time_slot)

    return 'test'


@app.route('/activities/<activity_name>', methods=['GET', 'POST'])
def render_activity(activity_name):
    activity = model.activity.get_one(_id=activity_name)
    if not activity:
        page_not_found('Activity not exists')
    #return activity['name']

@app.route('/register/<activity_name>', methods=['GET', 'POST'])
def reg_activity(activity_name):
    from helper.form import reg_form_wrapper
    activity = model.activity.get_one(_id=activity_name)

    if not activity:
        return render_template('error/404.html'), 404

    form = reg_form_wrapper(activity['time_slot'])

    if request.method == 'GET':
        if not 'user_id' in session:
            #User has not logged in
            return redirect(url_for('signin'))
        #Get current user
        cur_user = model.user.get_one(_id=session['user_id'])
        if not cur_user:
            #Should not occur unless something is wrong with session
            raise Exception('Unrecognized session user')
        if activity_name in cur_user['activity']:
            #User has already registered this activity
            return render_template('register/already_registered.html')
        else:
            return render_template('register/register.html', activity=activity, form=form)

    elif request.method == 'POST':
        activity = model.activity.get_one(_id=activity_name)
        if not form.validate():
            #Some filed is incorrect
            return render_template('register/register.html', activity=activity, form=form)
        else:
            #Get current user
            cur_user = model.user.get_one(_id=session['user_id'])
            work_dir = os.path.join(os.getcwd(), 'app/static/upload/user/'+activity_name)

            #Create folder if necessary
            upload_path = "static/upload/user/"+activity_name
            if not os.path.exists(work_dir):
                os.mkdir(work_dir)
            work_dir = os.path.join(work_dir, session['user_id'])
            upload_path = os.path.join(upload_path, session['user_id'])
            if not os.path.exists(work_dir):
                os.mkdir(work_dir)

            #Check upload file
            cv_file = request.files['cv']
            from helper.format import is_pdf, is_word
            cv_valid = True
            if not is_pdf(cv_file.mimetype) and not is_word(cv_file.mimetype):
                cv_valid = False

            if not cv_valid:
                #CV or ST is in wrong format
                form.cv.errors.append('Only word or pdf is allowed')
            else:
                #Check dangerous filename
                cv_file_name = secure_filename(cv_file.filename)
                cv_file_path = os.path.join(work_dir, cv_file_name)
                cv_upload_path = os.path.join(upload_path, cv_file_name)
                #Save file to work_dir
                cv_file.save(cv_file_path)

                #Insert participation to db
                participation = {}
                for item in request.form:
                    participation[item] = request.form[item]
                participation['cv'] = cv_upload_path
                participation.pop('csrf_token')
                model.user.add_activity(cur_user['_id'], activity_name, participation)
                return render_template('register/register_success.html')


@app.route('/myActivities')
def my_activities():
    if not 'user_id' in session:
        redirect(url_for('signin'))
    else:
        cur_user = model.user.get_one(_id=session['user_id'])
        if not cur_user:
            #Should not occur unless something is wrong with session
            raise Exception('Unrecognized session user')
        #Construct activities list
        user_activities = []
        for activity in cur_user['activity']:
            activity_inf = model.activity.get_one(_id=activity)
            activity_inf['user_inf'] = cur_user['activity'][activity]
            user_activities.append(activity_inf)
        return render_template('myactivities.html', activities=user_activities)


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
