# api_proxy/middleware.py
from django_prometheus.middleware import PrometheusAfterMiddleware

class AsyncPrometheusMiddleware(PrometheusAfterMiddleware):
    async def __call__(self, request):
        response = await self.get_response(request)
        self.process_response(request, response)
        return response