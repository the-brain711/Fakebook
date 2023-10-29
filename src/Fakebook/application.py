from flask import Flask
application = Flask(__name__) # This needs to be named `application`


@application.route("/")
def index():
    return "<h1>Hello DEV!</h1>"


@application.route("/another")
def another():
    return "<h1>Another Page!</h1>"


if __name__ == "__main__":
    application.run(debug=True)