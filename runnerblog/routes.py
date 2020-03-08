import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from runnerblog import app, db, bcrypt
from runnerblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from runnerblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

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
    # get all the posts from the database
    posts = Post.query.all()
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

@app.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()

    if form.validate_on_submit():
        post = Post(title = form.title.data, content = form.content.data, author = current_user)
        db.session.add(post)
        db.session.commit()
        
        flash("Post Created", "success")
        return redirect(url_for("home"))

    return render_template("create_post.html", title = "New Post", form = form, legend = "New Post")

@app.route("/post/<int:post_id>")
def post(post_id):
    # return the post or error page
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title = post.title, post = post)

@app.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
     # return the post or error page
    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
        # 403 for forbidden route
        abort(403)

    form = PostForm()
    
    # save the updated post to the database
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()

        flash("Post is updated", "success")
        return redirect(url_for("post", post_id = post.id))

    # populate the post form with data
    elif request.method == "GET":
        form = PostForm()
        form.title.data = post.title
        form.content.data = post.content

    return render_template("create_post.html", title = "Update Post", form = form, legend = "Update Post")

@app.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    # return the post or error page
    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
        # 403 for forbidden route
        abort(403)
    
    # remove the post from the database
    db.session.delete(post)

    # save the changes
    db.session.commit()

    flash("Post is removed", "success")
    return redirect(url_for("home"))