from flask import Flask
from flask_mysqldb import MySQL


def create_app():
    app = Flask(__name__)
    db = connect_db(app)

    # Change this to your secret key (it can be anything, it's for extra protection)
    app.config["SECRET_KEY"] = "secret"
    app.config["DATABASE"] = db
    
    # Import blueprints
    from .auth import auth
    from .views import views
    
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')

    return app


def connect_db(app):
    app.config["MYSQL_HOST"] = "fakebook-db.ch5ziarjkczw.us-east-1.rds.amazonaws.com"
    app.config["MYSQL_PORT"] = 3306
    app.config["MYSQL_USER"] = "admin"
    app.config["MYSQL_PASSWORD"] = "Fakebook!db01"
    app.config["MYSQL_DB"] = "fakebook_db"
    
    return MySQL(app)