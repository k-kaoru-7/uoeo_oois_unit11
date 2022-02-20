from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)

# Setting configuration
app.config.from_object('surgery.config')

# DB initialization
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Login Initialization
login = LoginManager(app)
login.login_view = 'login'

import surgery.routes