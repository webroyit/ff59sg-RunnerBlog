import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from runnerblog import app, db, bcrypt
from runnerblog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from runnerblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

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

# save the new image on the profile_pics
def save_picture(form_picture):
    # create a random string
    random_hex = secrets.token_hex(8)

    # get the file extension
    # name the variable _ if it does not get used
    _, f_ext = os.path.splitext(form_picture.filename)

    # new file name
    picture_fn = random_hex + f_ext

    # get the path for the new file to be saved
    picture_path = os.path.join(app.root_path, "static/profile_pics", picture_fn)

    # resize the image
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    # save the image
    i.save(picture_path)

    return picture_fn

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
    # redirect to home page if the user is alread login
    if current_user.is_authenticated:
        return redirect(url_for("home"))

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
    # redirect to home page if the user is alread login
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    # create instance of login form
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # login the user
            login_user(user, remember = form.remember.data)

            # args is a dictionary(object)
            # get() will return null if it empty
            next_page = request.args.get("next")

            # using ternary conditional
            # redirect the user of the last page they visited or home page
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash(f"Login failed, please try again", "danger")

    return render_template("login.html", title = "Login", form = form)

@app.route("/logout")
def logout():
    # logout the user
    logout_user()
    return redirect(url_for("home"))

@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()

    # change user information
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data

        # save the changes on the database
        db.session.commit()

        # flash message
        flash("Your account has been updated", "success")

        return redirect(url_for("account"))

    # prefill the account form data
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for("static", filename = "profile_pics/" + current_user.image_file)
    return render_template("account.html", title = "Account", image_file = image_file, form = form)