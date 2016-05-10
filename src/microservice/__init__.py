# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.mongoengine import MongoEngine
from pymongo import read_preferences


db = MongoEngine()


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    # Initiate mongoengine
    db.init_app(app)

    # Import blueprints
    from api.views import api as api_blueprint

    # Register blueprints
    app.register_blueprint(api_blueprint)

    return app

