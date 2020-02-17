from flask import Flask
# double underscore for the name of the module
app = Flask(__name__)

# you can add more endpoints to use the same function
@app.route("/")
@app.route("/home")
def hello():
    return "<h1>It Works</h1>"

@app.route("/about")
def about():
    return "<h1>About Page</h1>"

if __name__ == "__main__":
    # restart the server
    app.run(debug = True)