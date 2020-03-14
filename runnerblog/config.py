from runnerblog.configEnv import EMAIL, PASSWORD, SECRETKEY, SQLALCHEMYDATABASEURI

class Config:
    # secret key to protect against changing cookies and cross site request forgery attacks
    SECRET_KEY = SECRETKEY

    # location of the database on the file
    SQLALCHEMY_DATABASE_URI = SQLALCHEMYDATABASEURI

    # configure email
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = "587"
    MAIL_USE_TLS = "True"
    MAIL_USERNAME = EMAIL
    MAIL_PASSWORD = PASSWORD