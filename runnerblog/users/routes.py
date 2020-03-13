from flask import Blueprint

users = Blueprint("users", __name__)

@users.route("/register", methods=["GET", "POST"])
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

@users.route("/login", methods=["GET", "POST"])
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

@users.route("/logout")
def logout():
    # logout the user
    logout_user()
    return redirect(url_for("home"))

@users.route("/account", methods=["GET", "POST"])
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

@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get("page", 1, type = int)

    # filter_by() filter the data
    user = User.query.filter_by(username = username).first_or_404()

    posts = Post.query.filter_by(author = user).order_by(Post.date_posted.desc()).paginate(page = page, per_page = 5)
    
    return render_template("user_posts.html", posts = posts, user = user)

@users.route("/forgot_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = RequestResetForm()
    
    if form.validate_on_submit():
        # find user data by email
        user = User.query.filter_by(email = form.email.data).first()
        
        send_reset_email(user)

        flash("Check your email for instructions to reset your password", "info")
        return redirect(url_for("login"))

    return render_template("reset_request.html", title = "Forgot Password", form = form)

@users.route("/forgot_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    
    user = User.verify_reset_token(token)

    if user is None:
        flash("This token is invalid", "warning")
        return redirect(url_for("reset_request"))
    
    form = ResetPasswordForm()
    
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user.password = hashed_password
        db.session.commit()

        flash(f"Your password has been updated", "success")
        
        return redirect(url_for("login"))

    form = ResetPasswordForm()
    return render_template("reset_password.html", title = "Reset Password", form = form)