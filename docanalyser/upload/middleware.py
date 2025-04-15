import time
import logging

logger = logging.getLogger(__name__)

class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        logger.info(
            f"Request: {request.method} {request.path} "
            f"from IP: {request.META.get('REMOTE_ADDR')}"
        )

        response = self.get_response(request)

        duration = time.time() - start_time

        logger.info(
            f"Response: {request.method} {request.path} "
            f"Status: {response.status_code} "
            f"Duration: {duration:.2f}s"
        )

        return response