from .models.user import User
from .models.post import Post
from .models.enums import FriendRequestErrors
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

        user.timeline.view_timeline()
        posts = user.timeline.posts
        friend_requests = user.friend_requests
        
        if len(posts) != 0:
            return render_template(
                "home.html",
                username=session["username"],
                fullname=session["fullname"],
                posts=posts,
                friendrequests=friend_requests,
            )
        else:
            msg = "No Posts..."

    return render_template("home.html", fullname=session["fullname"], username=session["username"], msg=msg, friendrequests=friend_requests)


@views.route("/friends")
def friends():
    if "loggedin" in session:
        # Displays error message on website
        msg = ""

        if request.method == "GET":
            db = app.config["DATABASE"]
            user = User(db, session["id"])
            friends = user.friends_list.friends

            if friends:
                return render_template("friends.html", friends=friends, username=session["username"], fullname=session["fullname"])
            else:
                return render_template("friends.html", friends=None, username=session["username"], fullname=session["fullname"])
    else:
        msg = "Failed to load friends page"

    return render_template("friends.html", msg=msg, username=session["username"], fullname=session["fullname"])


@views.route("/search_user", methods=["GET"])
def search_user():
    # Display error message on website
    msg = ""
    
    # Check if POST request has at least a post description
    if (
        "loggedin" in session
        and request.method == "GET"
        and "searchbar" in request.args
        and "searchbar-submit" in request.args
    ):
        username = request.args["searchbar"]
        db = app.config["DATABASE"]
        user = User(db, session["id"])
        searched_user = user.search_for_user(username)
        
        if searched_user:
            render_template("profile.html", searcheduser=searched_user)
        else:
            msg = "Failed to find user " + username
    else:
        msg = "User search failed..."
    return render_template("profile.html", msg=msg)


@views.route("/send_friend_request", methods=["POST"])
def send_friend_request():
    # Display error message on website
    msg = ""

    # Check if POST request has at least a post description
    if (
        "loggedin" in session
        and request.method == "POST"
        and "searchbox-friends" in request.form
    ):
        friend_username = request.form["searchbox-friends"]
        db = app.config["DATABASE"]

        user = User(db, session["id"])
        status = user.send_friend_request(friend_username)

        if status == FriendRequestErrors.INVALID_USER:
            msg = "Could not find user: " + friend_username
        elif status == FriendRequestErrors.FRIEND_REQUEST_ALREADY_EXISTS:
            msg = "Friend request for " + friend_username + " already exists."
        else:
            return redirect(url_for("views.friends"))
    else:
        msg = "Unable to send friend request..."

    return render_template("friends.html", msg=msg)


@views.route("/accept_friend_request", methods=["POST"])
def accept_friend_request():
    # Display error message on website3
    msg = ""

    # Check if it's a POST request when clicking the like button
    if (
        "loggedin" in session
        and request.method == "POST"
        and "friend-id" in request.form
        and "accept-friend-request" in request.form
    ):
        friend_id = int(request.form["friend-id"])

        db = app.config["DATABASE"]
        user = User(db, session["id"])
        user.friend_requests[friend_id].accept_friend_request()

        return redirect(url_for("views.home"))
    else:
        msg = "Failed to accept friend request"

    return render_template("home.html", msg=msg)


@views.route("/decline_friend_request", methods=["POST"])
def decline_friend_request():
    # Display error message on website3
    msg = ""

    # Check if it's a POST request when clicking the like button
    if (
        "loggedin" in session
        and request.method == "POST"
        and "friend-id" in request.form
        and "decline-friend-request" in request.form
    ):
        friend_id = int(request.form["friend-id"])

        db = app.config["DATABASE"]
        user = User(db, session["id"])
        user.friend_requests[friend_id].decline_friend_request()

        return redirect(url_for("views.home"))
    else:
        msg = "Failed to decline friend request"

    return render_template("home.html", msg=msg)


@views.route("/profile")
def profile():
    if "loggedin" in session:
        db = app.config["DATABASE"]
        user = User(db, session["id"])

        return render_template("profile.html", user=user, username=session["username"], fullname=session["fullname"])


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
        post.get_comments()

        if post:
            return render_template("post.html", post=post, username=session["username"], fullname=session["fullname"])
        else:
            msg = "Failed to view comments."
    else:
        msg = "Failed to view comments."

    return render_template("post.html", msg=msg)


@views.route("/comment", methods=["POST"])
def comment():
    # Display error message on website
    msg = ""

    if (
        "loggedin" in session
        and request.method == "POST"
        and "post-id" in request.form
        and "comment-textbox" in request.form
    ):
        post_id = request.form["post-id"]
        comment_text = request.form["comment-textbox"]

        db = app.config["DATABASE"]
        user = User(db, session["id"])
        user.make_comment(post_id, comment_text)

        # Crashes when uncommented. Need to fix
        # post = Post(db=db, post_id=post_id)
        # return render_template("post.html", post=post)

        return redirect(url_for("views.home"))

    elif "loggedin" in session and request.method == "POST":
        msg = "Text is required to make a comment."
    else:
        msg = "Unable to make a comment..."

    return render_template("post.html", msg=msg)


@views.route("/reply", methods=["POST"])
def reply():
    # Display error message on website
    msg = ""

    if (
        "loggedin" in session
        and request.method == "POST"
        and "post-id" in request.form
        and "comment-id" in request.form
        and "reply-textbox" in request.form
    ):
        post_id = request.form["post-id"]
        comment_id = request.form["comment-id"]
        reply_text = request.form["reply-textbox"]

        db = app.config["DATABASE"]
        user = User(db, session["id"])
        user.reply_to_comment(post_id, comment_id, reply_text)

        # Crashes when uncommented. Need to fix
        # post = Post(db=db, post_id=post_id)
        # return render_template("post.html", post=post)

        return redirect(url_for("views.home"))

    elif "loggedin" in session and request.method == "POST":
        msg = "Text is required to make a comment."
    else:
        msg = "Unable to make a comment..."

    return render_template("post.html", msg=msg)
