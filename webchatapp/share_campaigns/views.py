# share_campaigns/views.py

from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import login_user, current_user, logout_user, login_required
from webchatapp import db
from webchatapp.models import ShareTemplate
from webchatapp.share_campaigns.forms import ShareTemplateForm, DownloadUploadForm


campaigns = Blueprint('campaigns', __name__) # and passing the buildin name variable __name__

@campaigns.route('/share_campaigns/using_form', methods=['GET','POST'])
def using_form():
    form = ShareTemplateForm()

    if form.validate_on_submit():
        share_template = ShareTemplate(
            country_code=form.country_code.data,
            contact_number=form.contact_number.data,
            template_name=form.template_name.data,
            upload_file=form.upload_file.data.filename if form.upload_file.data else None
        )
        
        db.session.add(share_template)
        db.session.commit()
        flash('Share Template data added successfully')
        return redirect(url_for('campaigns.share_campaigns'))
    
    return render_template('using_form.html', form=form)


@campaigns.route('/share_campaigns/using_csv', methods=['GET', 'POST'])
def using_csv():
    form = DownloadUploadForm()

    if form.validate_on_submit():
        # Process the form submission here, e.g., save uploaded files, etc.
        # You can access form.upload_csv.data and form.upload_images.data for the uploaded files
        flash('Files uploaded successfully')
        return redirect(url_for('campaigns.share_campaigns'))  # Redirect to the same page after processing
    
    return render_template('using_csv.html', form=form)


# Share campaign route with added pagination functionality
@campaigns.route('/share_campaigns')
@campaigns.route('/share_campaigns/<int:page>')
def share_campaigns(page=1):
    per_page = 10  # Number of items per page
    campaigns = ShareTemplate.query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template('share_campaigns.html', campaigns=campaigns)


# @campaigns.route('/share_campaigns')
# def share_campaigns():
#     campaigns = ShareTemplate.query.all()  # Query all data from the database
#     return render_template('share_campaigns.html', campaigns=campaigns)