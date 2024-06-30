# chat_settings >> forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed    # used for profile picture.


class ChatSettingForm(FlaskForm):
    idle_notification_time = StringField('Idle Notification Time (in minutes)', validators=[DataRequired()])
    idle_notification_message = StringField('Idle Notification Message', validators=[DataRequired()])
    idle_chat_end_time = StringField('Idle Chat End Time (in minutes)', validators=[DataRequired()])
    end_chat_message = StringField('End Chat Message', validators=[DataRequired()])
    submit = SubmitField('Update')