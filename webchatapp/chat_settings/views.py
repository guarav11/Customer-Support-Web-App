# chat_settings/views.py

from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import login_user, current_user, logout_user, login_required
from webchatapp import db
from webchatapp.models import ChatSetting
from webchatapp.chat_settings.forms import ChatSettingForm


chatsettings = Blueprint('chatsettings', __name__) # and passing the buildin name variable __name__

@chatsettings.route('/chat_settings', methods=['GET','POST'])
def chat_setting():
    chat_settings = ChatSetting.query.first()  # Assuming there's only one chat setting in the database, adjust this if needed

    if chat_settings:
        form = ChatSettingForm(obj=chat_settings)
    else:
        form = ChatSettingForm()

    if form.validate_on_submit():
        if not chat_settings:
            chat_settings = ChatSetting(
                idle_notification_time=form.idle_notification_time.data,
                idle_notification_message=form.idle_notification_message.data,
                idle_chat_end_time=form.idle_chat_end_time.data,
                end_chat_message=form.end_chat_message.data
            )
            db.session.add(chat_settings)
        else:
            chat_settings.idle_notification_time = form.idle_notification_time.data
            chat_settings.idle_notification_message = form.idle_notification_message.data
            chat_settings.idle_chat_end_time = form.idle_chat_end_time.data
            chat_settings.end_chat_message = form.end_chat_message.data

        db.session.commit()
        flash('Chat settings updated successfully.')
        return redirect(url_for('users.chats'))  # Redirect to an appropriate view function

    return render_template('chat_setting.html', form=form)



# def chat_setting():
#     form = ChatSettingForm()

#     if form.validate_on_submit():
#         chat_settings = ChatSetting(
#             idle_notification_time=form.idle_notification_time.data,
#             idle_notification_message=form.idle_notification_message.data,
#             idle_chat_end_time=form.idle_chat_end_time.data,
#             end_chat_message=form.end_chat_message.data
#         )
        
#         db.session.add(chat_settings)
#         db.session.commit()
#         flash('Chat settings updated successfully.')
#         return redirect(url_for('users.chats'))  # Redirect to an appropriate view function
#     return render_template('chat_setting.html', form=form)

