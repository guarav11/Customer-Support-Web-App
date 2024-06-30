# users/views.py

from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import login_user, current_user, logout_user, login_required
from webchatapp import db
from flask import current_app
from webchatapp.models import User
from webchatapp.users.forms import RegisterationForm, UpdateUserForm, LoginForm, ResetPasswordForm, ForgotPasswordForm
from flask_mail import Message
from itsdangerous import URLSafeSerializer
from webchatapp.email import mail

from webchatapp.conversations import EventFetcher


users = Blueprint('users', __name__)  # and passing the buildin name variable __name__


@users.route('/register', methods=['GET','POST'])
def register():
    form = RegisterationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    password=form.password.data,
                    username=form.username.data)
        
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)

        
@users.route('/', methods=['GET','POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            # flash('Login successful')
            return render_template('chats.html')
        else:
            flash('Invalid email or password. Please try again.', 'error')
            
    return render_template('login.html', form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("users.login"))

# @users.route('/chats')
# def chats():
#     return render_template('chats.html')

@users.route('/chats', methods=['GET'])
def chats():
    messages = EventFetcher.fetch_text_by_event()
    return render_template('chats.html', messages=messages)



@users.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@users.route('/analytics')
def analytics():
    return render_template('analytics.html')

@users.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
            flash('An email has been sent with instructions to reset your password.')
            return redirect(url_for('users.login'))
        else:
            flash('No account found with that email address.')
    return render_template('forgot_password.html', form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.verify_reset_token(token)
    if not user:
        flash('Invalid or expired token.')
        return redirect(url_for('users.forgot_password'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('users.login'))

    return render_template('reset_password.html', form=form)


# Create the message to be sent
def send_password_reset_email(user):
    token = generate_reset_token(user)  # You need to implement this
    msg = Message('Password Reset Request',
                  sender='your-email@example.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_password', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


def generate_reset_token(user, expires_sec=1800):
    s = URLSafeSerializer(current_app.config['SECRET_KEY'])
    return s.dumps({'user_id': user.id}, salt='reset-password')








# account (update UserForm)
@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():

    form = UpdateUserForm()

    if form.validate_on_submit():

        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            flash("Username already exists")
            return redirect(url_for("users.account"))
        
        # if form.picture.data:
        #     username = current_user.username
        #     pic = add_profile_pic(form.picture.data, username)
        #     current_user.profile_image = pic

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('User Account Updated.')
        return redirect(url_for("users.account"))
    
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    # grap the profile image and render it back to account page
    # profile_image = url_for('static', filename='profile_pics/'+current_user.profile_image)
    return render_template('account.html', form=form)



# @users.route("/<username>")
# def user_posts(username):
#     page = request.args.get('page', 1, type=int)
#     user = User.query.filter_by(username=username).first_or_404()
#     blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page, per_page=3)
#     return render_template('user_blog_posts.html', blog_posts=blog_posts, user=user)


