import os
import logging

from api.utils.custom_logging.logging_setup import logging_setup
from api.app_factory import create_app


# Set up logging
logging_setup()
logger = logging.getLogger(__name__)

# Condition config based off flask env
flask_env = os.environ.get('FLASK_ENV')
if flask_env == 'development':
    from api.config import DevelopmentConfig
    app, api = create_app(DevelopmentConfig)
elif flask_env == 'production':
    from api.config import ProductionConfig
    app, api = create_app(ProductionConfig)
elif flask_env == 'testing':
    # Default to testing
    # Usually means we are running the app locally
    from api.config import TestingConfig
    logger.warning('No FLASK_ENV set, defaulting to TestingConfig')
    app, api = create_app(TestingConfig)
else:
    raise RuntimeError('No FLASK_ENV set')

from api.routes.health_check_routes import HealthCheckRoutes

# Add the roots to the API
api.add_resource(HealthCheckRoutes, '/health_check')

if __name__ == '__main__':
    app.run()
