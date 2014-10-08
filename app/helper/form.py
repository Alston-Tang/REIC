__author__ = 'tang'
from wtforms import TextField, PasswordField, SubmitField, SelectField
from wtforms import validators, ValidationError
from flask_wtf import Form
from app import model


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

    def validate_email(form, field):
        user_exist = model.user.get(email=field.data)
        if user_exist:
            raise ValidationError("Email is already taken")
