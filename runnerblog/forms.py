from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from runnerblog.models import User

class RegistrationForm(FlaskForm):
    # DataRequired() = input cannot be empty
    # Length() =  length of the input
    # Email() = check if the input is an email
    # EqualTo() = check if the password and confirm password match
    username = StringField("Username", validators = [DataRequired(), Length(min = 3, max = 20)])
    email = StringField("Email", validators = [DataRequired(), Email()])
    password = PasswordField("Password", validators = [DataRequired(), Length(min = 6, max = 20)])
    confirm_password = PasswordField("Confirm Password", validators = [DataRequired(), EqualTo("password"), Length(min = 6, max = 20)])
    submit = SubmitField("Create Account")

    # custom validation
    def validate_username(self, username):
        # find the user in the database
        user = User.query.filter_by(username = username.data).first()

        if user:
            # send a message
            raise ValidationError("Username aleady existed")

    def validate_email(self, email):
        # find the email in the database
        user = User.query.filter_by(email = email.data).first()

        if user:
            raise ValidationError("Email aleady existed")

class LoginForm(FlaskForm):
    email = StringField("Email", validators = [DataRequired(), Email()])
    password = PasswordField("Password", validators = [DataRequired(), Length(min = 6, max = 20)])
    remember = BooleanField("Remember me")
    submit = SubmitField("Login")

class UpdateAccountForm(FlaskForm):
    # FileField is field for file type
    # FileAllowed is a validation for file type
    username = StringField("Username", validators = [DataRequired(), Length(min = 3, max = 20)])
    email = StringField("Email", validators = [DataRequired(), Email()])
    picture = FileField("Update Profile Picture", validators = [FileAllowed(["jpg", "png"])])
    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username = username.data).first()

            if user:
                raise ValidationError("Username aleady existed")

    def validate_email(self, email):
        if email.data != current_user.username:
            user = User.query.filter_by(email = email.data).first()

            if user:
                raise ValidationError("Email aleady existed")

class PostForm(FlaskForm):
    title = StringField("Title", validators = [DataRequired()])
    content = TextAreaField("Content", validators = [DataRequired()])
    submit = SubmitField("Post")