# email.py

import os
from dotenv import load_dotenv
from flask_mail import Mail

load_dotenv()  # Load environment variables from .env file

mail = Mail()

# Configure mail settings
def configure_mail(app):
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Gmail SMTP server
    app.config['MAIL_PORT'] = 587  # Port for TLS
    app.config['MAIL_USE_TLS'] = True  # Enable TLS
    app.config['MAIL_USERNAME'] = os.environ.get('GMAIL_USERNAME')  # Your Gmail email address
    app.config['MAIL_PASSWORD'] = os.environ.get('GMAIL_PASSWORD')  # Your Gmail password

    mail.init_app(app)

