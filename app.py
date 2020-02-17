from flask import Flask
# double underscore for the name of the module
app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1>It Works</h1>"

if __name__ == "__main__":
    # restart the server
    app.run(debug = True)