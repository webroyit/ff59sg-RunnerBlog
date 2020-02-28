from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

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
login_manager.login_view = "login"

from runnerblog import routes