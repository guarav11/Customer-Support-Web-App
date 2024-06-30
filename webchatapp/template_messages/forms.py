# template_messages >> forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
from wtforms.widgets import TextArea
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed    # used for profile picture.


class AddTemplateForm(FlaskForm):
    template_name = StringField('Template Name', validators=[DataRequired()])
    template_message = StringField('Template Message', widget=TextArea(), validators=[DataRequired()])
    submit = SubmitField('Submit')
