from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

# double underscore for the name of the module
app = Flask(__name__)

# secret key to protect against changing cookies and cross site request forgery attacks
app.config["SECRET_KEY"] = "d5bcb19fb808ef171f39f4a2a6c5c466"

# location of the database on the file
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    image_file = db.Column(db.String(20), nullable = False, default = "default.jpg")
    password = db.Column(db.String(60), nullable = False)

    # adding one to many relationship
    # backref create a new column
    # lazy to load the data from the database when it is needed
    posts = db.relationship("Post", backref = "author", lazy = True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False,  default = datetime.utcnow)      # no () after utcnow otherwise the time will set when the server start
    content = db.Column(db.Text, nullable = False)

    # get the user id from the User class
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

posts = [
    {
        "author": "Bob Test",
        "title": "First Time Running",
        "content": "It was fun to run around",
        "date_posted": "Feb 15, 2020"
    },
    {
        "author": "Rob Run",
        "title": "Running At the Park",
        "content": "I enjoyed running at the park",
        "date_posted": "Feb 17, 2020"
    }
]

# you can add more endpoints to use the same function
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts = posts)

@app.route("/about")
def about():
    return render_template("about.html", title = "About")

@app.route("/register", methods=["GET", "POST"])
def register():
    # create instance of registration form
    form = RegistrationForm()
    if form.validate_on_submit():
        # display a message on the client
        # secound arugment is the styles
        flash(f"Account created for {form.username.data}! Welcome", "success")
        
        return redirect(url_for("home"))

    return render_template("register.html", title = "Register", form = form)

@app.route("/login", methods=["GET", "POST"])
def login():
    # create instance of login form
    form = LoginForm()

    if form.validate_on_submit():
        # for testing
        if form.email.data == "test@testing.com" and form.password.data == "123456":
            flash(f"Welcome back!", "success")
            return redirect(url_for("home"))
        else:
            flash(f"Login failed, please try again", "danger")

    return render_template("login.html", title = "Login", form = form)

if __name__ == "__main__":
    # restart the server
    app.run(debug = True)