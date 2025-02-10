import os

from dotenv import load_dotenv
from flask import Flask, Response, jsonify, make_response, redirect, request

from backend_db import getPhotoUser, photoProcess
from login import (addFriend, checkUserAccess, getUser, login, newUser,
                   removeFriend, removeFriendRequest, sendFriendRequest,
                   userExists, validLogin)
from posts import createPost, singleUserFeed
from projects import (createProject, getProject, getProjectPosts,
                      getUserProjects, projectAccessCheck)

# Load env keys
load_dotenv()

app = Flask(__name__, static_folder="/", static_url_path="/")
app.secret_key = os.getenv("FLASK_SECRET_KEY")
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")


@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/public/<file>")
def public(file: str):
    return app.send_static_file(f"public/{file}")


@app.route("/postphotos/<photofile>")
def photophotos(photofile: str):
    """Collects photos from the backend for users."""
    user_cookie = request.cookies.get("auth_token")
    if validLogin(user_cookie):
        user_doc = getUser(user_cookie)
        user = user_doc["username"] if user_doc else False
    else:
        return "Invalid Login Token", 401

    # Check authentication logic.
    photo_owner = getPhotoUser(photofile)

    if not checkUserAccess(user, photo_owner):
        return "Not authorized to view this photo.", 401

    file = photoProcess(photofile)

    if file:
        return Response(
            file.read(),
            content_type=file.content_type,
            headers={"Content-Disposition": f'inline; filename="{file.filename}"'},
        )
    else:
        return jsonify({"error": "Image not found."})


@app.route("/getUserPosts/<username>", methods=["POST"])
def getUserPosts(username: str):
    """Returns all of the posts for a user."""
    data = request.get_json()
    token = data.get("token")
    if validLogin(token):
        user_doc = getUser(token)
        user = user_doc["username"] if user_doc else False
        if not user:
            return "Please relogin."
        return singleUserFeed(user, username)
    return "invalid login token."


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
    username, token = login(username_or_email, pwd)
    if username != False:
        response = make_response(jsonify({"username": username, "token": token}), 200)
        response.set_cookie(
            "auth_token",
            value=token,
            httponly=True,
            secure=True,
            samesite="Strict",
        )
        return response
    return jsonify({"username": "", "token": ""}), 401


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


@app.route("/createPost", methods=["POST"])
def processPost():
    """Processes a user's new post."""
    token = request.form.get("token")
    # Check valid token.
    if not validLogin(token):
        return "Invalid login token.", 401

    title = request.form.get("title")
    description = request.form.get("description")
    project = request.form.get("project")
    image = request.files["post-image"]
    startDate = request.form.get("start-date")
    endDate = request.form.get("end-date")
    user_doc = getUser(token)
    user = user_doc["username"] if user_doc else False
    if user:
        createPost(user, title, description, startDate, endDate, image, project)
    return redirect("/Profile")


@app.route("/createProject", methods=["POST"])
def processProject():
    """Processes new project requests."""
    token = request.form.get("token")
    # Check valid token.
    if not validLogin(token):
        return "Invalid login token.", 401
    title = request.form.get("project_title")
    description = request.form.get("description")
    image = request.files["project-image"]
    user_doc = getUser(token)
    user = user_doc["username"] if user_doc else False
    startDate = request.form.get("start-date")
    endDate = request.form.get("end-date")
    if user:
        createProject(user, title, description, image, startDate, endDate)
    return redirect("/Profile")


@app.route("/UserProjects", methods=["POST"])
def userProjects():
    """Returns a list of mappings with the user's project information."""
    data = request.get_json()
    token = data.get("token")
    # Check valid token.
    if not validLogin(token):
        return "Invalid login token.", 401
    user_doc = getUser(token)
    user = user_doc["username"] if user_doc else False
    return getUserProjects(user)


@app.route("/project/<username>/<project_id>", methods=["POST"])
def projectPage(username: str, project_id: str):
    """This function returns data related to single projects."""
    data = request.get_json()
    token = data.get("token")
    # Check valid token.
    if not validLogin(token):
        return "Invalid login token.", 401
    user_doc = getUser(token)
    search_user = user_doc["username"] if user_doc else False
    project = getProject(username, project_id)
    project_title = project["project_title"] if project else None
    if not projectAccessCheck(
        project_title,
        username,
        search_user,
    ):
        return "Not valid access to view the page.", 401

    project["posts"] = getProjectPosts(username, project_title)
    return jsonify(project)


@app.route("/find_user/<username>", methods=["GET", "POST"])
def searchFriends(username: str):
    # NOTE: Need to switch to getting the token from the data not the cookies to avoid CORS.
    token = request.cookies.get("auth_token")
    if not validLogin(token):
        return "Invalid login token.", 401

    user_doc = getUser(token)
    loggedInUser = user_doc["username"] if user_doc else False
    if loggedInUser == username:
        return jsonify({"UserExists": True, "AddedFriend": False, "SameUser": True})

    if userExists(username):
        if username in user_doc["friends"]:
            return jsonify(
                {"UserExists": True, "AlreadyFriend": True, "AddedFriend": False}
            )
        request_sent = sendFriendRequest(loggedInUser, username)
        if request_sent:
            return jsonify(
                {"UserExists": True, "AlreadyFriend": False, "AddedFriend": True}
            )
    return jsonify({"UserExists": False})


@app.route("/friend_requests", methods=["GET", "POST"])
def returnFriendRequests():
    token = request.cookies.get("auth_token")
    if not validLogin(token):
        return "Invalid login token.", 401
    user_doc = getUser(token)
    if not user_doc:
        return "Invalid login", 401
    requests = user_doc["friend_requests"] if "friend_requests" in user_doc else []
    return jsonify(requests)


@app.route("/friendlist", methods=["GET", "POST"])
def friendList():
    token = request.cookies.get("auth_token")
    if not validLogin(token):
        return "Invalid login token.", 401
    user_doc = getUser(token)
    if not user_doc:
        return "Invalid login", 401
    requests = user_doc["friends"] if "friends" in user_doc else []
    return jsonify(requests)


@app.route("/process_friend_request", methods=["GET", "POST"])
def processFriendRequest():
    """This helps users add friends."""
    data = request.get_json()
    token = data.get("token")

    if not validLogin(token):
        return "Invalid login token.", 401
    user_doc = getUser(token)

    target_user = data.get("target_user")
    add_or_remove = data.get("add_or_remove")

    app.logger.info(
        f"Info: User: {user_doc['username']}, add_or_remove: {add_or_remove}, target_user: {target_user}"
    )

    if add_or_remove == "add" and target_user in user_doc["friend_requests"]:
        addFriend(user_doc["username"], target_user)
        removeFriendRequest(user_doc["username"], target_user)
        return "success", 200
    elif add_or_remove == "remove" and target_user in user_doc["friends"]:
        removeFriend(user_doc["username"], target_user)
        return "success", 200

    return "Doesn't make sense", 400


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)  # Turn off debug in prod.
