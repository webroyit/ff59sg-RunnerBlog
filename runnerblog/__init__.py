from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from runnerblog.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

# redirect the user to the login page is they are not login
login_manager.login_view = "users.login"

# change the color of the flash message
login_manager.login_message_category = "info"

mail = Mail()

# initialize the extensions at the top of the file
def create_app(config_class = Config):
    # double underscore for the name of the module
    app = Flask(__name__)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # use the variables from config.py
    app.config.from_object(Config)

    # access to these routes
    from runnerblog.users.routes import users
    from runnerblog.posts.routes import posts
    from runnerblog.main.routes import main

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)

    return app