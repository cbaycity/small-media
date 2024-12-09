from flask import Flask, request, redirect, jsonify
from feed import createFeed
from login import newUser, login, validLogin, getUser
from posts import createPost
from projects import createProject, getUserProjects

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
def public(file: str):
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
    email = request.form.get("email", None)
    pwd = request.form.get("password")
    username_new, email_new = newUser(user, email, pwd)
    if username_new and email_new:
        return redirect("/login")
    return redirect(
        f"/signup?email_taken={str(email_new).lower()}&username_taken={str(username_new).lower()}"
    )


@app.route("/userLogin", methods=["POST"])
def userLogin():
    data = request.get_json()
    username_or_email = data["username"]
    pwd = data["password"]
    status, token = login(username_or_email, pwd)
    if status:
        return jsonify({"token": token}), 200
    return jsonify({"token": ""}), 401


@app.route("/validLogin", methods=["GET", "POST"])
def validToken():
    """Checks if the current user token is valid."""
    data = request.get_json()
    token = data.get("token")
    if token is None:
        return jsonify({"valid": False}), 200
    if validLogin(token):
        return jsonify({"valid": True}), 200
    return jsonify({"valid": False}), 489


@app.route("/createPost", method=["POST"])
def processPost():
    """Processes a user's new post."""
    token = request.form.get("token")
    # Check valid token.
    if ~validToken(token):
        return "Invalid login token.", 401

    title = request.form.get("post-title")
    description = request.form.get("description")
    project = request.form.get("project")
    image = request.files["post-image"]
    user = getUser(token)
    if user:
        createPost(user, title, description, image, project)
    return redirect("/Profile")


@app.route("/createProject", method=["POST"])
def processProject():
    """Processes new project requests."""
    token = request.form.get("token")
    # Check valid token.
    if ~validToken(token):
        return "Invalid login token.", 401
    title = request.form.get("project-title")
    description = request.form.get("description")
    image = request.files["project-image"]
    user = getUser(token)
    if user:
        createProject(user, title, description, image)
    return redirect("/Profile")


@app.route("/UserProjects", method=["POST"])
def userProjects():
    """Returns a list of a user's projects"""
    data = request.get_json()
    token = data.get("token")
    # Check valid token.
    if ~validToken(token):
        return "Invalid login token.", 401
    user = getUser(token)
    return getUserProjects(user)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)  # Turn off debug in prod.
