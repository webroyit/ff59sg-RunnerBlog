from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
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