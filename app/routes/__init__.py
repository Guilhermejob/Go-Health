from flask import Flask
from app.routes.client_blueprint import bp_clients


def init_app(app: Flask):
    app.register_blueprint(bp_clients)
