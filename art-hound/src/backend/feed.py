"""A module containing code to create feeds as requested by website users."""

import json


def createFeed(user, feed_type):
    """Processes user feed requests.

    Inputs:
        user (str):
        feed_type (str):

    """
    # TODO: Adjust the input types to process backend queries.

    with open("sample-assets/bayard-post-one/post-data.json", "r") as file:
        post_one = json.load(file)

    with open("sample-assets/bayard-post-two/post-data.json", "r") as file:
        post_two = json.load(file)

    with open("sample-assets/bayard-post-three/post-data.json", "r") as file:
        post_three = json.load(file)

    return [post_one, post_two, post_three]
