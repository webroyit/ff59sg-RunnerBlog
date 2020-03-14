from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from runnerblog.configEnv import EMAIL, PASSWORD

# double underscore for the name of the module
app = Flask(__name__)

# secret key to protect against changing cookies and cross site request forgery attacks
app.config["SECRET_KEY"] = "d5bcb19fb808ef171f39f4a2a6c5c466"

# location of the database on the file
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

# redirect the user to the login page is they are not login
login_manager.login_view = "users.login"

# change the color of the flash message
login_manager.login_message_category = "info"

# configure email
app.config["MAIL_SERVER"] = "smtp.googlemail.com"
app.config["MAIL_PORT"] = "587"
app.config["MAIL_USE_TLS"] = "True"
app.config["MAIL_USERNAME"] = EMAIL
app.config["MAIL_PASSWORD"] = PASSWORD
mail = Mail(app)

# access to these routes
from runnerblog.users.routes import users
from runnerblog.posts.routes import posts
from runnerblog.main.routes import main

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)