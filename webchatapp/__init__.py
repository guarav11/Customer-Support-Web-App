# webchatapp/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from webchatapp.email import configure_mail
import os

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'users.login'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'mysecretkey'
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from webchatapp.users.views import users
    from webchatapp.agents.views import agents
    from webchatapp.template_messages.views import templates
    from webchatapp.share_campaigns.views import campaigns
    from webchatapp.chat_settings.views import chatsettings

    app.register_blueprint(users)
    app.register_blueprint(agents)
    app.register_blueprint(templates)
    app.register_blueprint(campaigns)
    app.register_blueprint(chatsettings)

    configure_mail(app)

    return app








# # webchatapp/__init__.py

# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from flask import flash
# from flask_login import LoginManager
# import os
# from flask_mail import Mail, Message   # to support reset password mailing functionality


# app = Flask(__name__)

# ################################
# # Database Setup #
# ################################
# # Set a secret key for form security
# app.config['SECRET_KEY'] = 'mysecretkey'

# # Configure the SQLite database
# basedir = os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# # Initialize SQLAlchemy and Flask-Migrate
# db = SQLAlchemy(app)
# Migrate(app, db)


# ###################################
# # Login Configurations
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'users.login'


# from webchatapp.users.views import users
# from webchatapp.agents.views import agents
# from webchatapp.template_messages.views import templates
# from webchatapp.share_campaigns.views import campaigns
# from webchatapp.chat_settings.views import chatsettings
# # from puppycompanyblog.error_pages.handlers import error_pages

# # register blueprint
# app.register_blueprint(users)
# app.register_blueprint(agents)
# app.register_blueprint(templates)
# app.register_blueprint(campaigns)
# app.register_blueprint(chatsettings)
