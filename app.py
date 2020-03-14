from runnerblog import create_app

app = create_app()

if __name__ == "__main__":
    # restart the server
    app.run(debug = True)