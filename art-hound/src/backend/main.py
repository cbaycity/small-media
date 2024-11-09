from flask import Flask, request
from feed import createFeed

app = Flask(__name__, static_folder="../", static_url_path="/")


@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/public/<file>")
def public(file):
    return app.send_static_file(f"client/public/{file}")


@app.route("/members")
def members():
    return ["Bayard", "Sean", "Eamon"]


@app.route("/createAccount")
def createAccount():
    """Creates a new account if the username and email don't already exist."""
    return True


@app.route("/feed")
def feed():
    """Returns a list of JSON objects"""
    return createFeed(request.headers.get("USER_INFO"), request.headers.get("FEEDTYPE"))


@app.route("/postphotos/<photofile>")
def photoprocess(photofile: str):
    """Collects photos from the backend for users."""
    # TODO: Remove the hard coding and actually process requests.
    return app.send_static_file(f"backend/sample-assets/bayard-post-one/{photofile}")


if __name__ == "__main__":
    app.run(debug=True)  # Need to turn off when in production.
