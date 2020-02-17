from flask import Flask, render_template
# double underscore for the name of the module
app = Flask(__name__)

# you can add more endpoints to use the same function
@app.route("/")
@app.route("/home")
def hello():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    # restart the server
    app.run(debug = True)