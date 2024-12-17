"""A module for managing image processing."""

from backend_db import DB, FS

USERS = DB["users"]
POSTS = DB["posts"]
PROJECTS = DB["projects"]


def process_image(username, requested_image):
    """Determine if the image can be viewed by the user requesting it, if so, return the image."""
    # Check if image is in projects or posts.
    post_doc = POSTS.find_one({"image-id": requested_image})
    projects_doc = PROJECTS.find_one({"image-id": requested_image})

    image_doc = post_doc if post_doc else projects_doc
    if image_doc is None:
        return "Image not found."

    if "public" in image_doc and image_doc["public"]:
        print(f"Return type of FS query: {type(FS.get(requested_image))}")
        return FS.get(requested_image).read()

    image_owner = USERS.find_one({"username": image_doc["username"]})

    if "public" in image_owner and image_owner["public"]:
        print(f"Return type of FS query: {type(FS.get(requested_image))}")
        return FS.get(requested_image).read()

    if username in image_owner["friends"]:
        print(f"Return type of FS query: {type(FS.get(requested_image))}")
        return FS.get(requested_image).read()

    return "Not authorized to view this image."
