from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm

# double underscore for the name of the module
app = Flask(__name__)

# secret key to protect against changing cookies and cross site request forgery attacks
app.config["SECRET_KEY"] = "d5bcb19fb808ef171f39f4a2a6c5c466"

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

@app.route("/login")
def login():
    # create instance of login form
    form = LoginForm()
    return render_template("login.html", title = "Login", form = form)

if __name__ == "__main__":
    # restart the server
    app.run(debug = True)