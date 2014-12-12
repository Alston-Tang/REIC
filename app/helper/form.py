__author__ = 'tang'
from wtforms import TextField, PasswordField, SubmitField, SelectField, StringField, FileField
from wtforms import validators, ValidationError
from flask_wtf import Form
from app.model import User
from magic import Magic


class SignIn(Form):
    email = TextField('Email')
    password = PasswordField('Password')
    submit = SubmitField('submit')


class SignUp(Form):
    email = TextField('Email', [validators.Email(), validators.Required()])
    password = PasswordField('Password', [validators.Required(), validators.Length(min=8)])
    password_confirm = PasswordField('Password confirm', [validators.Required(), validators.EqualTo('password')])
    username = TextField('Username', [validators.Required(), validators.Length(min=4, max=20)])
    tel = TextField('Telephone', [validators.Optional(), validators.Regexp(r'^\d{8,15}$')])
    sid = TextField('SID', [validators.Required(), validators.Regexp(r'^\d{10}$')])
    dept = TextField('Department', [validators.Optional(), validators.Length(max=20)])
    year = SelectField('Year', [validators.Optional()], choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)],
                       coerce=int)
    college = TextField('College', [validators.Optional()])
    submit = SubmitField('submit')

    @staticmethod
    def validate_email(form, field):
        user_exist = User.exist(field.data)
        if user_exist:
            raise ValidationError("Email is already taken")


def reg_form_wrapper(time_slot_inf):
    choices = []
    for time_num in time_slot_inf:
        choices.append((str(time_num[0]), str(time_num[0])))

    class RegForm(Form):
        email = TextField('Email', [validators.Required(), validators.Email()])
        tel = TextField('Telephone', [validators.Required(), validators.Regexp(r'^\d{8,15}$')])
        sid = TextField('SID', [validators.Required(), validators.Regexp(r'^1155\d{6}$')])
        dept = TextField('Department', [validators.Required(), validators.Length(max=20)])
        year = SelectField('Year', [validators.Required()], choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)],
                           coerce=int)
        college = TextField('College', [validators.Required()])
        cv = FileField('CV', [validators.Required()])
        time_slot = SelectField('1st preference', [validators.Required()], choices=choices)
        time_slot2 = SelectField('2nd preference', [validators.Required()], choices=choices)
        time_slot3 = SelectField('3rd preference', [validators.Required()], choices=choices)
        submit = SubmitField('submit')
    return RegForm()


class RegForm(Form):
    def __init__(self, time_slot, *args, **kwargs):
        choices = []
        for time_num in time_slot:
            choices.append((str(time_num[0]), str(time_num[0])))
        self.time_slot = SelectField('Time slot', [validators.Required()], choices=choices)
        super(RegForm, self).__init__(*args, **kwargs)

    email = TextField('Email', [validators.Required(), validators.Email()])
    tel = TextField('Telephone', [validators.Required(), validators.Regexp(r'^\d{8,15}$')])
    sid = TextField('SID', [validators.Required(), validators.Regexp(r'^1155\d{6}$')])
    dept = TextField('Department', [validators.Required(), validators.Length(max=20)])
    year = SelectField('Year', [validators.Required()], choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)],
                       coerce=int)
    college = TextField('College', [validators.Optional()])
    cv = FileField('CV', [validators.Required()])
    st = FileField('ST', [validators.Required()])
    submit = SubmitField('submit')




