import os
import logging
from flask import Flask
from flask_restful import Api
from api.database import db


logger = logging.getLogger(__name__)

def create_app(config_class):
    logger.info('Configuring application')

    app = Flask(__name__)
    logger.info(f'Configuring application with {config_class}')
    app.config.from_object(config_class)

    # Set up the API
    api = Api(app)

    # Set up the database
    logger.info('Configuring database')
    db.init_app(app)

    return app, api

