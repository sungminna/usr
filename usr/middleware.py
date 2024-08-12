import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('drf')


class RequestLoggingMiddleware(MiddlewareMixin):

    def process_request(self, request):
        logger.info(f"Received {request.method} request to {request.get_full_path()}")

    def process_response(self, request, response):
        logger.info(f"Returned {response.status_code} response")
        return response
