from flask import Flask, request, redirect
from feed import createFeed
from login import newUser, login, checkLogin
from flask_wtf import CSRFProtect
import secrets

app = Flask(__name__, static_folder="/", static_url_path="/")
app.secret_key = secrets.token_hex(98)
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
    user = request.form.get("username")
    email = request.form.get("password")
    pwd = request.form.get("email")
    username_new, email_new = newUser(user, email, pwd)
    if username_new and email_new:
        return redirect("/login")
    return redirect(
        f"/signup?email_taken={str(email_new).lower()}&username_taken={str(username_new).lower()}"
    )


@app.route("/login", methods=["POST"])
def userLogin():
    username_or_email = request.form.get("username")
    pwd = request.form.get("password")
    if login(username_or_email, pwd):
        return True
    return False  # Need to return regular HTML codes for invalid credentials.


@app.route("/validLogin", methods=["GET", "POST"])
def login():
    # Validate user credentials (e.g., from request.json)
    username = request.json.get("username")
    password = request.json.get("password")

    if username == "valid_user" and password == "valid_pass":
        response = make_response(jsonify({"message": "Login successful"}))
        response.set_cookie(
            "auth_token",
            "your_secure_token",
            httponly=True,
            samesite="Strict",
            secure=True,
        )
        return response
    else:
        return jsonify({"error": "Invalid credentials"}), 401


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)  # Turn off debug in prod.
