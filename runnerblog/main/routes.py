from flask import render_template, request, Blueprint
from runnerblog.models import User, Post

main = Blueprint("main", __name__)

# you can add more endpoints to use the same function
@main.route("/")
@main.route("/home")
def home():
    # type = int to return a error if value is not int type
    page = request.args.get("page", 1, type = int)

    # get some posts per page
    # per_page for number of post for each page
    # order_by() to sort the data
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page = page, per_page = 5)
    
    return render_template("home.html", posts = posts)

@main.route("/about")
def about():
    return render_template("about.html", title = "About")