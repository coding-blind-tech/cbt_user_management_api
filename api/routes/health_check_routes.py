import logging

from flask_restful import Resource

logger = logging.getLogger(__name__)


class HealthCheckRoutes(Resource):
    """Health check routes"""

    def get(self):
        """Health check"""

        logger.info('HealthCheckRoutes invoked')
        return {'status': 'OK'}, 200
