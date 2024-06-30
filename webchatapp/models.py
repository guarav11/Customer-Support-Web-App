# Import necessary modules and components
from webchatapp import db, login_manager  # Importing the database instance and login manager
from werkzeug.security import generate_password_hash, check_password_hash  # Importing password hashing functions
from flask_login import UserMixin  # Importing UserMixin for user authentication
from datetime import datetime  # Importing datetime module for timestamping

from flask import current_app
from itsdangerous import URLSafeSerializer

# Define a function to load a user by ID for the login manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Define the User model class
class User(db.Model, UserMixin):
    __tablename__ = 'users'  # Table name for the User model

    # Define columns for the User table
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    # Define relationship with BlogPost model
    # posts = db.relationship('BlogPost', backref='author', lazy=True)

    # Constructor to initialize User object
    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    # Method to check password validity
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Representation of User object
    def __repr__(self):
        return f"Username {self.username}"
    
    # Method to verify the password reset token
    @staticmethod
    def verify_reset_token(token):
        s = URLSafeSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token, salt='reset-password')
            user_id = data['user_id']
        except:
            return None
        return User.query.get(user_id)
    
    # Method to set the password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)


# Define the Agent model class
class Agent(db.Model, UserMixin):
    __tablename__ = 'agent'  # Table name for the Agent model

    # Define columns for the Agent table
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    name = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    agent_type = db.Column(db.String(64), index=True)

    # Define relationship with BlogPost model
    # posts = db.relationship('BlogPost', backref='author', lazy=True)

    # Constructor to initialize Agent object
    def __init__(self, name, email, password, agent_type):
        self.name = name
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.agent_type = agent_type

    # Method to check password validity
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Representation of Agent object
    def __repr__(self):
        return f"name {self.name}"
    

# Define the Template model class
class Template(db.Model):
    __tablename__ = 'template'  # Table name for the Template model

    # Define columns for the Template table
    id = db.Column(db.Integer, primary_key=True)
    template_name = db.Column(db.String(100), unique=True, nullable=False)
    template_message = db.Column(db.Text, nullable=False)

    # Constructor to initialize Template object
    def __init__(self, template_name, template_message):
        self.template_name = template_name
        self.template_message = template_message

    # Representation of Template object
    def __repr__(self):
        return f'Template Name: {self.template_name}, Template Message: {self.template_message}'
    

# Define the ShareTemplate model class
class ShareTemplate(db.Model):
    __tablename__ = 'share_template'

    id = db.Column(db.Integer, primary_key=True)
    country_code = db.Column(db.String(100), nullable=False)
    contact_number = db.Column(db.String(100), nullable=False)
    template_name = db.Column(db.String(100), unique=True, nullable=False)
    upload_file = db.Column(db.String(255), nullable=True)

    def __init__(self, country_code, contact_number, template_name, upload_file):
        self.country_code = country_code
        self.contact_number = contact_number
        self.template_name = template_name
        self.upload_file = upload_file

    def __repr__(self):
        return f'Country Code: {self.country_code}, Contact Number: {self.contact_number}, Template Name: {self.template_name}, Upload File: {self.upload_file}'
    

# Define the ChatSetting model class
class ChatSetting(db.Model):
    __tablename__ = 'chat_setting'

    id = db.Column(db.Integer, primary_key=True)
    idle_notification_time = db.Column(db.String(100), nullable=False)
    idle_notification_message = db.Column(db.String(300), nullable=False)
    idle_chat_end_time = db.Column(db.String(100), nullable=False)
    end_chat_message = db.Column(db.String(300), nullable=False)

    def __init__(self, idle_notification_time, idle_notification_message, idle_chat_end_time, end_chat_message):
        self.idle_notification_time = idle_notification_time
        self.idle_notification_message = idle_notification_message
        self.idle_chat_end_time = idle_chat_end_time
        self.end_chat_message = end_chat_message

    def __repr__(self):
        return f'Idle Notification Time: {self.idle_notification_time}, Idle Notification Message: {self.idle_notification_message}, Idle Chat End Time: {self.idle_chat_end_time}, End Chat Message: {self.end_chat_message}'