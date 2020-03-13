import os
import secrets
from PIL import Image
from flask import url_for
from runnerblog import app, mail
from flask_mail import Message

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

# email the user with a link to the reset password page
def send_reset_email(user):
    token = user.get_reset_token()

    # subject of the email
    msg = Message("Password Reset Request from Runnerblog", sender = "roywebweb123@gmail.com", recipients = [user.email])
    
    # _external to get the full domain
    msg.body = f'''Click on the following link to reset password:
{url_for('users.reset_token', token = token, _external = True)}

Ignore this email if you did not request password change.
'''
    # send the email with the message
    mail.send(msg)