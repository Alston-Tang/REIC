# coding=utf-8
__author__ = 'Tang'

from flask import render_template, url_for, request, redirect, session
from app import app, file, model
from time import time
from datetime import datetime
from bson import ObjectId, errors
from werkzeug import secure_filename
from helper.session import decompose_user, admin_session
import json
import os

from model import *


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
def sign_in():
    from app.helper.form import SignIn

    form = SignIn()
    if request.method == 'GET':
        return render_template("signin.html", title='Sign In', nav_bar=app.nav_bar, form=form)
    if request.method == 'POST':
        cur_user = User(email=request.form['email'], password=request.form['password']).valid()
        if cur_user:
            # Since ObjectId is not serializable
            # TODO Any better solution?
            session['user'] = decompose_user(cur_user)
            return redirect(url_for('index'))
        else:
            return render_template("signin.html", title='Sign In', nav_bar=app.nav_bar, form=form,
                                   error="Invalid Username or Password")


# log out handler
@app.route('/signOut', methods=['GET', 'POST'])
def sign_out():
    session.pop('user', None)
    return redirect(url_for('index'))


"""
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
"""

# signup handler
@app.route('/signUp', methods=['GET', 'POST'])
def sign_up():
    from app.helper.form import SignUp

    form = SignUp(request.form)
    if request.method == 'GET':
        return render_template('signup.html', form=form)
    elif request.method == 'POST':
        if form.validate():
            # Copy form data to user information dictionary
            new_user = User()
            for key, value in request.form.items():
                if key in User.fields_list:
                    new_user.attr[key] = value
            # Validate whether this user is member of REIC according to SID
            new_user.attr['member'] = Member(sid=int(request.form['sid'])).exist()
            # SHA1 password
            new_user.attr['password'] = User.pwd_hash(new_user.attr['password'])

            # Save user to database
            rv = new_user.commit()
            if not rv:
                # Come to here when insert is failed due to db error
                return render_template('error/unexpected_error.html')
            session['user'] = decompose_user(new_user)
            return redirect(url_for('index'))
        else:
            return render_template('signup.html', form=form)


# Management Portal
@app.route('/manage/portal')
def manage_portal():
    if not admin_session(session):
        return render_template('error/permission_denied.html')
    return render_template('manage/portal.html', User=User, Member=Member, Activity=Activity, Section=Section,
                           Page=Page)


@app.route('/manage/members', methods=['GET', 'POST', 'DELETE', 'PUT'])
def manage_members():
    if not admin_session(session):
        return render_template('error/permission_denied.html')
    from helper.form import MemberInf

    member_form = MemberInf(request.form)
    if request.method == 'GET':
        return render_template('manage/member.html', Member=Member, form=member_form,
                               nav_bar_right=app.nav_bar.get_member_extra())
    elif request.method == 'DELETE':
        member_id = request.form['id']
        member_to_remove = Member(ObjectId(member_id))
        if not member_to_remove.attach:
            return json.dumps({"error": "Member id can not be found"})
        rv = member_to_remove.destroy()
        if not rv:
            return json.dumps({"error": "Failed: database error"})
        return json.dumps({"success": True, "id": member_id, "count": Member.count()})
    elif request.method == 'PUT':
        print(request.form)
        if member_form.validate():
            member_id = request.form.get('id', "")
            edit_member = None
            if member_id:
                edit_member = Member(ObjectId(member_id))
                if not edit_member.attach:
                    return json.dumps({"error": "Member id can not be found"})
            else:
                edit_member = Member()
            edit_member.set(request.form)
            rv = edit_member.commit()
            if not rv or not edit_member.attach:
                return json.dumps({"error": "Failed: database error"})
            return json.dumps({"success": True, "member": edit_member.attr, "count": Member.count()}, default=str)
        else:
            return json.dumps({"error": "Invalid Input", "error_inf": member_form.errors})


# Editor load and save handle
@app.route('/manage/editor', methods=['GET', 'POST'])
def editor():
    if not admin_session(session):
        return render_template('error/permission_denied.html')
    if request.method == 'GET':
        section_id = request.args.get('sec', None)
        section = Section(ObjectId(section_id))
        if section.attach:
            return render_template('edit.html', section=section.attr['content'],
                                   nav_bar=app.nav_bar.get_editor(),
                                   create_time=section.attr['create_time'],
                                   id=section_id, creator=section.attr['creator'],
                                   modified_time=section.attr['modified_time'],
                                   nav_bar_right=app.nav_bar.get_editor_extra())
        else:
            return render_template('edit.html', create=True, create_time=datetime.today(),
                                   nav_bar=app.nav_bar.get_editor(),
                                   modified_time=datetime.today(), id="",
                                   nav_bar_right=app.nav_bar.get_editor_extra())
    if request.method == 'POST':
        # Get upload information
        section_id = request.form.get('id', "")
        title = request.form.get('title', "")
        create_time = datetime.strptime(request.form.get('create_time', datetime.today().strftime('%Y/%m/%d %H:%M')),
                                        '%Y/%m/%d %H:%M')
        modified_time = datetime.today()
        content = request.form.get('content', "")
        preview_img = request.form.get('preview_img', False)
        # Check
        if content == "":
            return json.dumps({'error': 'Empty content'})
        if title == "":
            return json.dumps({'error': 'Empty title'})
        # Check end
        # If it is a new section
        if section_id == "":
            # Update preview image
            img_model = PreviewImg(data=preview_img)
            img_id = img_model.commit()
            if not img_id:
                return json.dumps({'error': 'Insert preview image failed at db'})
            new_id = Section(title=title, create_time=create_time, modified_time=modified_time,
                             content=content, creator=session['user']['username'], preview_img=img_id).commit()
            if new_id:
                return json.dumps({'success': True, 'id': str(new_id)})
            else:
                return json.dumps({'error': 'Insert section failed at db'})
        # else it is an existing section
        else:
            section = Section(ObjectId(section_id))
            if not section.attach:
                # Can not find that section
                # TODO Write a error to log
                return False
            # Update Preview Image
            # If an existing image do not have a preview image
            if not section.attr['preview_img']:
                # Create an preview image
                new_img_id = PreviewImg(data=preview_img).commit()
                if not new_img_id:
                    # TODO Write a warning to log
                    pass
                else:
                    section.attr['preview_img'] = new_img_id
            else:
                exist_img = PreviewImg(section.attr['preview_img'])
                if not exist_img:
                    # TODO Write a error to log
                    pass
                else:
                    exist_img.attr['data'] = preview_img
                    rv = exist_img.commit()
                    if rv.get("n", False) != 1:
                        return json.dumps({'error': 'Unexpected update'})
            # Update modified_time
            section.attr['modified_time'] = modified_time
            # Update title
            section.attr['title'] = title
            # Update content
            section.attr['content'] = content
            # Save to db
            section.commit()
            return json.dumps(({'success': True, 'id': section_id}))


@app.route('/manage/sections', methods=['GET', 'DELETE'])
def manage_sections():
    if not admin_session(session):
        return render_template('error/permission_denied.html')
    if request.method == 'GET':
        page_id = request.args.get('page', None)
        section_overview = []
        sections = Section.find(join=True)
        # Reassemble sections container
        for section in sections:
            section_overview.append(section.attr)

        return render_template("manage/section.html",
                               sections=section_overview,
                               nav_bar_right=app.nav_bar.get_section_extra())
    if request.method == 'DELETE':
        section_to_delete = Section(ObjectId(request.form['id']))
        if section_to_delete.destroy():
            return json.dumps({'success': True})
        else:
            return json.dumps({'error': "DB_exception"})


@app.route('/manage/pages', methods=['GET', 'DELETE'])
def manage_pages():
    if not admin_session(session):
        return render_template('error/permission_denied.html')
    if request.method == 'GET':
        page_overview = []
        pages = Page.find()
        # Reassemble pages container
        for page in pages:
            page_overview.append(page.attr)
        return render_template("manage/page.html",
                               pages=page_overview,
                               nav_bar_right=app.nav_bar.get_page_extra())
    elif request.method == 'DELETE':
        page_to_delete = Page(ObjectId(request.form['id']))
        if page_to_delete.destroy():
            return json.dumps({'success': True})
        else:
            return json.dumps({'error': "DB_exception"})


@app.route('/manage/page_editor', methods=['GET', 'POST'])
def page_editor():
    if not admin_session(session):
        return render_template('error/permission_denied.html')
    if request.method == 'GET':
        page_id = request.args.get('page', None)
        required_page = Page(ObjectId(page_id))
        sections = Section.find(join=True)
        section_input = []
        for section in sections:
            section_input.append(section.attr)
        if required_page.attach:
            required_page.join()
            return render_template('manage/page_editor.html', sections=section_input,
                                   required_page=required_page.attr,
                                   nav_bar_right=app.nav_bar.get_editor_extra())
        else:
            return render_template('manage/page_editor.html', sections=section_input,
                                   required_page=None,
                                   nav_bar_right=app.nav_bar.get_editor_extra())
    elif request.method == 'POST':
        data = request.form.get('data', "[]")
        title = request.form.get('title', "untitled")
        # Transfer data from json to list
        data = json.loads(data)
        # For each object id in list, transfer from unicode string to ObjectId
        obj_data = []
        for item in data:
            obj_data.append(ObjectId(item))
        data = obj_data
        page_id = request.form.get('id', "")
        if not data:
            # No data error
            return json.dumps({'error': "A page should at least contain one section"})
        # Try to create object id, if error happens, create a new id
        try:
            page_id = ObjectId(page_id)
        except errors.InvalidId:
            page_id = ObjectId()
        # Create model
        relevant_page = Page(page_id)
        if relevant_page.attach:
            # The page exists
            relevant_page.attr['section'] = data
            relevant_page.attr['modified_time'] = datetime.today()
            relevant_page.attr['title'] = title
            relevant_page.commit()
        else:
            # Create a new page
            relevant_page.attr['section'] = data
            relevant_page.attr['modified_time'] = datetime.today()
            relevant_page.attr['create_time'] = datetime.today()
            relevant_page.attr['title'] = title
            relevant_page.commit()

        # Finally update navigation bar
        from nav_bar import NavBar

        app.nav_bar = NavBar()
        # Return success json
        return json.dumps({'success': True, "id": str(relevant_page.attr['_id'])})


"""
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
    for int_day in range(29, 31):
        for hour in range(9, 12):
            time_slot.append(datetime(2014, 11, int_day, hour, 0))
            time_slot.append(datetime(2014, 11, int_day, hour, 30))
        for hour in range(13, 17):
            time_slot.append(datetime(2014, 11, int_day, hour, 0))
        time_slot.append(datetime(2014, 11, int_day, hour, 30))
        time_slot.append(datetime(2014, 11, int_day, 17))
    print(time_slot)
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
        # return activity['name']


@app.route('/stat/<activity_name>')
def stat_activity(activity_name):
    from model import activity, user

    activity_exist = activity.get_one(name=activity_name)
    # If activity doesn't exist, display 404
    if not activity_exist:
        return render_template('error/404.html'), 404

    # Else check role first
    #If user haven't logged in, redirect to sign in page
    if not "user_id" in session:
        return redirect(url_for('signin'))
    #Get user information
    cur_user = user.get_one(_id=session['user_id'])
    if not cur_user:
        #Some thing wrong happen here
        print ("Error when getting user's information")
        return render_template('error/unexpected_error.html'), 404
    #If user is not an administrator
    role = cur_user.get("role", "")
    if role != "admin":
        return render_template('error/permission_denied.html')
    #User's role is administrator, construct display page
    render_content = []
    users = user.get()
    for each_user in users:
        if activity_name in each_user['activity']:
            temp = {}
            for k, v in each_user['activity'][activity_name].iteritems():
                temp[k] = v
            temp['member'] = each_user['member']
            render_content.append(temp)

    return render_template('stat/showreg.html', participants=render_content)



@app.route('/register/<activity_name>', methods=['GET', 'POST'])
def reg_activity(activity_name):
    from helper.form import reg_form_wrapper

    activity = Activity(activity_name)

    if not activity.attach:
        return render_template('error/404.html'), 404

    form = reg_form_wrapper(activity.attr['time_slot'])

    if request.method == 'GET':
        if 'user' not in session:
            # User has not logged in
            return redirect(url_for('signin'))
        # Get current user
        cur_user = User(session['user']['_id'])
        if not cur_user.attach:
            # Should not occur unless something is wrong with session
            # TODO Change exception
            raise Exception('Unrecognized session user')
        if activity_name in cur_user.attr['activity']:
            # User has already registered this activity
            return render_template('register/already_registered.html')
        else:
            return render_template('register/register.html', activity=activity, form=form)

    elif request.method == 'POST':
        activity = model.activity.get_one(_id=activity_name)
        if not form.validate():
            # Some filed is incorrect
            return render_template('register/register.html', activity=activity, form=form)
        else:
            # Get current user
            cur_user = model.user.get_one(_id=session['user_id'])
            work_dir = os.path.join(os.getcwd(), 'app/static/upload/user/' + activity_name)

            # Create folder if necessary
            upload_path = "static/upload/user/" + activity_name
            if not os.path.exists(work_dir):
                os.mkdir(work_dir)
            work_dir = os.path.join(work_dir, session['user_id'])
            upload_path = os.path.join(upload_path, session['user_id'])
            if not os.path.exists(work_dir):
                os.mkdir(work_dir)

            # Check upload file
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
            # Should not occur unless something is wrong with session
            raise Exception('Unrecognized session user')
        # Construct activities list
        user_activities = []
        for activity in cur_user['activity']:
            activity_inf = model.activity.get_one(_id=activity)
            activity_inf['user_inf'] = cur_user['activity'][activity]
            user_activities.append(activity_inf)
        return render_template('myactivities.html', activities=user_activities)
"""

# no rule matched, then treat it as a page
@app.route('/<page_title>')
def render_page(page_title):
    require_pages = Page.find({"title": page_title}, join=True)
    if require_pages:
        if len(require_pages) > 1:
            # TODO Write a warning to log
            pass
        return render_template('index.html', title=page_title, page=require_pages[0].attr,
                               nav_bar=app.nav_bar.get_structure())
    else:
        return page_not_found("")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404