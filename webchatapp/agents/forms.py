# agents >> forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed    # used for profile picture.

# from flask_login import current_user
from webchatapp.models import  Agent


class AddAgentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    agent_type = StringField('Agent Type', validators=[DataRequired()])
    submit = SubmitField('Submit')


class EditAgentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    agent_type = StringField('Agent Type', validators=[DataRequired()])
    password = PasswordField('New Password')
    confirm_password = PasswordField('Confirm New Password', validators=[EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Update')

    def validate_email(self, field):
        agent = Agent.query.filter_by(email=field.data).first()
        if agent and agent.id != self.agent_id:
            raise ValidationError('This email is already registered as an agent.')

    def __init__(self, agent_id, *args, **kwargs):
        super(EditAgentForm, self).__init__(*args, **kwargs)
        self.agent_id = agent_id