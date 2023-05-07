from flask import Flask

from . import constants
from .extensions import db


def create_app():
    app = Flask(__name__)
    username = constants.DB_USERNAME
    password = constants.DB_PASSWORD
    host = constants.DB_HOST
    port = constants.DB_PORT
    name = constants.DB_NAME
    app.config["SQLALCHEMY_DB_URI"] = f"postgresql://{username}:{password}@{host}:{port}/{name}"
    db.init_app(app)
    return app


app = create_app()
