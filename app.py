from flask import Flask
# double underscore for the name of the module
app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1>It Works</h1>"