import os
import json
import logging

from flask import Flask, request, jsonify

LOG_LEVEL = str(os.getenv("LOG_LEVEL", "WARN")).upper()
logging.basicConfig(level=LOG_LEVEL)
logging.root.setLevel(LOG_LEVEL)


def rollback(data):
    print(f"{data}")


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import api

    app.register_blueprint(api.bp)

    from . import ready

    app.register_blueprint(ready.bp)

    return app
