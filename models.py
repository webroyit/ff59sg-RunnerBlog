from datetime import datetime
from __main__ import db

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