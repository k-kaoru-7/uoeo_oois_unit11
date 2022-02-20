import os

"""
This script defines configuration used in the application
"""

# Setting for DB
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
# Setting for secret key to protect against CSRF
SECRET_KEY = os.urandom(24)