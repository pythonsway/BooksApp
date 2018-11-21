import os

from flask import Flask
from flask_session import Session

from BooksApp import auth, books, db


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # Typical dealing with variables
    # app.config.from_object('config')
    # app.config.from_pyfile('config.py')


    app.config.from_mapping(SECRET_KEY=os.getenv("SECRET_KEY"),
                            DATABASE_URL=os.getenv("DATABASE_URL"),)

    # Configure session to use filesystem
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    app.register_blueprint(auth.bp)
    app.register_blueprint(books.bp)

    app.add_url_rule('/', endpoint='index')

    return app
