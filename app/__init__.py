from flask import Flask
from os import getenv, path, mkdir
from app.configs import database, migrations
from app import routes

def create_app():

    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = getenv("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JSON_SORT_KEYS"] = False
    FILES_DIRECTORY = f"app/{getenv('FILES_DIRECTORY')}"

    if not path.isdir(FILES_DIRECTORY):
        mkdir(FILES_DIRECTORY)

    database.init_app(app)
    migrations.init_app(app)
    routes.init_app(app)

    return app
