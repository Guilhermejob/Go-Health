from flask import Flask
from os import getenv
from app.configs import database, migrations, auth
from app import routes
from app import exceptions
from dotenv import load_dotenv

load_dotenv()

def create_app():

    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = getenv("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JSON_SORT_KEYS"] = False
    app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024
    app.config["SECRET_KEY"] = getenv("SECRET_KEY")

    database.init_app(app)
    migrations.init_app(app)
    auth.JWTManager(app)
    routes.init_app(app)
    exceptions.init_app(app)

    return app
