from flask import Flask, request, redirect
from feed import createFeed
from login import newUser, login

# from flask_wtf import CSRFProtect
from dotenv import load_dotenv
import os

# Load env keys
load_dotenv()

app = Flask(__name__, static_folder="/", static_url_path="/")
app.secret_key = os.getenv("FLASK_SECRET_KEY")
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
# Need to protect against Cross-site request forgery.
# Ignoring this for now.
# CSRFProtect(app)


@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/public/<file>")
def public(file):
    return app.send_static_file(f"public/{file}")


@app.route("/feed")
def feed():
    """Returns a list of JSON objects"""
    return createFeed(request.headers.get("USER_INFO"), request.headers.get("FEEDTYPE"))


@app.route("/postphotos/<photofile>")
def photoprocess(photofile: str):
    """Collects photos from the backend for users."""
    # TODO: Remove the hard coding and actually process requests.
    return app.send_static_file(f"sample-assets/bayard-post-one/{photofile}")


@app.route("/createAccount", methods=["POST"])
def accountCreation():
    user = request.form.get("username", None)
    email = request.form.get("password", None)
    pwd = request.form.get("email")
    username_new, email_new = newUser(user, email, pwd)
    if username_new and email_new:
        return redirect("/login")
    return redirect(
        f"/signup?email_taken={str(email_new).lower()}&username_taken={str(username_new).lower()}"
    )


@app.route("/userLogin", methods=["POST"])
def userLogin():
    username_or_email = request.form.get("username")
    pwd = request.form.get("password")
    status, token = login(username_or_email, pwd)
    if status:
        return token, 200
    return "", 401


@app.route("/validLogin", methods=["GET", "POST"])
def validLogin():
    """Checks if the current user token is valid."""
    return True  # Need to update.


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)  # Turn off debug in prod.
