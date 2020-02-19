from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtfomrs.validators import DataRequired, Length, Email, EqualTo

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

class LoginForm(FlaskForm):
    email = StringField("Email", validators = [DataRequired(), Email()])
    password = PasswordField("Password", validators = [DataRequired(), Length(min = 6, max = 20)])
    remember = BooleanField("Remember me")
    submit = SubmitField("Login")