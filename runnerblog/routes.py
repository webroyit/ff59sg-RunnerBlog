import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from runnerblog import app, db, bcrypt, mail
from runnerblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, RequestResetForm, ResetPasswordForm
from runnerblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

# you can add more endpoints to use the same function
@app.route("/")
@app.route("/home")
def home():
    # type = int to return a error if value is not int type
    page = request.args.get("page", 1, type = int)

    # get some posts per page
    # per_page for number of post for each page
    # order_by() to sort the data
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page = page, per_page = 5)
    
    return render_template("home.html", posts = posts)

@app.route("/about")
def about():
    return render_template("about.html", title = "About")