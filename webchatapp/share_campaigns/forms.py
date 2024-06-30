# template_messages >> forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
from wtforms.widgets import TextArea
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed    # used for profile picture.


class ShareTemplateForm(FlaskForm):
    country_code = StringField('Country Code', validators=[DataRequired()])
    contact_number = StringField('Contact Number', validators=[DataRequired()])
    template_name = StringField('Template Name', validators=[DataRequired()])
    upload_file = FileField('Upload File', validators=[FileAllowed(['pdf', 'doc', 'docx', 'png', 'jpg', 'jpeg'])])
    submit = SubmitField('Create')

class DownloadUploadForm(FlaskForm):
    upload_csv = FileField('Upload CSV File', validators=[FileAllowed(['csv'])])
    upload_images = FileField('Upload Images', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    import_button = SubmitField('Import')
