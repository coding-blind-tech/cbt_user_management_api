import os
import logging

logger = logging.getLogger(__name__)

username = os.environ.get('DB_USERNAME')
password = os.environ.get('DB_PASSWORD')
database_name = os.environ.get('DB_NAME')
database_host = os.environ.get('DB_HOST')
database_port = os.environ.get('DB_PORT')

if not username or not password or not database_name or not database_host or not database_port:
    raise ValueError('Please set the environment variables for the database connection')


class Config:
    """Base configuration"""

    logger.info('Configuring base configuration')
    SQLALCHEMY_DATABASE_URI = f'postgresql://{username}:{password}@{database_host}:{database_port}/{database_name}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable modification tracking


class TestingConfig(Config):
    """ Testing configuration - enables testing mode """

    logger.info('Configuring testing configuration')

    # Not typical, but importing the testing.postgresql here
    # To avoid having to install for running anything other than tests
    from testing.postgresql import Postgresql
    TESTING = True
    DEBUG = True
    postgresql = Postgresql()
    db_params = postgresql.dsn()
    SQLALCHEMY_DATABASE_URI = f"postgresql://{db_params['user']}@{db_params['host']}:{db_params['port']}/{database_name}"


class DevelopmentConfig(Config):
    """Development configuration - enables debug mode """

    logger.info('Configuring development configuration')
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration - disables debug mode"""

    DEBUG = False
