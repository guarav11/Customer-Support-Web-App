# users >> forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed    # used for profile picture.

from flask_login import current_user
from webchatapp.models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class RegisterationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', message='Pass must match')])
    pass_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def check_email(self, field):
        if User.query.filter_by(email = field.data).first():
            raise ValidationError('Your email has already been registered!')
        
    def check_username(self, field):
        if User.query.filter_by(username = field.data).first():
            raise ValidationError('Your username has already been registered!')
        
class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('There is no account with that email. You must register first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired(), Length(min=6), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired()])
    submit = SubmitField('Reset Password')

# class ResetPasswordForm(FlaskForm):
#     password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
#     confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
#     submit = SubmitField('Reset Password')



class UpdateUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    # picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def check_email(self, field):
        if User.query.filter_by(email = field.data).first():
            raise ValidationError('Your email has already been registered!')
        
    def check_username(self, field):
        if User.query.filter_by(username = field.data).first():
            raise ValidationError('Your username has already been registered!')