from .models.user import User
from .models.post import Post
from flask import current_app as app
from flask import Blueprint, render_template, redirect, request, url_for, session


views = Blueprint("views", __name__)


@views.route("/")
def home():
    if "loggedin" not in session:
        return redirect(url_for("auth.login"))

    # Displays error message on website
    msg = ""

    if request.method == "GET":
        db = app.config["DATABASE"]
        user = User(db, session["id"])
        username = user.username
        posts = user.timeline.view_timeline()

        if len(posts) != 0:
            return render_template("home.html", username=user.username, posts=posts)
        else:
            msg = "No Posts..."

    return render_template("home.html", username=username, msg=msg)


@views.route("/profile")
def profile():
    if "loggedin" in session:
        db = app.config["DATABASE"]
        user = User(db, session["id"])

        return render_template("profile.html", username=user.username, email=user.email)


@views.route("/create_post", methods=["POST"])
def create_post():
    # Display error message on website
    msg = ""

    # Check if POST request has at least a post description
    if (
        "loggedin" in session
        and request.method == "POST"
        and "create-post-textbox" in request.form
    ):
        post_description = request.form["create-post-textbox"]
        # Check if there's a post media (this is optional)
        # post_media = request.form["create-post-media"]
        db = app.config["DATABASE"]
        user = User(db, session["id"])
        user.make_post(post_description)

        return redirect(url_for("views.home"))

    elif "loggedin" in session and request.method == "POST":
        msg = "Post description is required to create a post."
    else:
        msg = "Unable to create post..."

    return render_template("home.html", msg=msg)


@views.route("/like_post", methods=["POST"])
def like_post():
    # Display error message on website3
    msg = ""

    # Check if it's a POST request when clicking the like button
    if (
        "loggedin" in session
        and request.method == "POST"
        and "post-id" in request.form
        and "like-post-submit" in request.form
    ):
        post_id = request.form["post-id"]

        db = app.config["DATABASE"]
        user = User(db, session["id"])
        user.like_post(post_id=post_id)

        return redirect(url_for("views.home"))
    else:
        msg = "Failed to like post"

    return render_template("home.html", msg=msg)


@views.route("/view_comments", methods=["GET"])
def view_comments():
    # Display error message on website3
    msg = ""

    # Check if it's a POST request when clicking the like button
    if (
        "loggedin" in session
        and request.method == "GET"
        and "post-id" in request.args
        and "comment-post-submit" in request.args
    ):
        post_id = request.args["post-id"]

        db = app.config["DATABASE"]
        post = Post(db, post_id=post_id)
        
        if post:
            return render_template("post.html", post=post)
        else:
            msg = "Failed to view comments."
    else:
        msg = "Failed to view comments."

    return render_template("post.html", msg=msg)
