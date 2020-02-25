from flask import render_template, url_for, flash, redirect
from runnerblog import app, db, bcrypt
from runnerblog.forms import RegistrationForm, LoginForm
from runnerblog.models import User, Post

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
        # hash the user password
        # decode() to change from bytes to string
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        
        user = User(username = form.username.data, email = form.email.data, password = hashed_password)
        
        db.session.add(user)
        db.session.commit()

        # display a message on the client
        # secound arugment is the styles
        flash(f"Account created! Please login", "success")
        
        return redirect(url_for("login"))

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
