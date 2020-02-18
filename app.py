from flask import Flask, render_template
# double underscore for the name of the module
app = Flask(__name__)

posts = [
    {
        "author": "Bob Test",
        "title": "First Time Running",
        "content": "It was fun to run around",
        "date_posted": "Feb 15, 2020"
    },
    {
        "author": "Rob Run",
        "title": "Running At the Park",
        "content": "I enjoyed running at the park",
        "date_posted": "Feb 17, 2020"
    }
]

# you can add more endpoints to use the same function
@app.route("/")
@app.route("/home")
def hello():
    return render_template("home.html", posts = posts)

@app.route("/about")
def about():
    return render_template("about.html", title = "About")

if __name__ == "__main__":
    # restart the server
    app.run(debug = True)