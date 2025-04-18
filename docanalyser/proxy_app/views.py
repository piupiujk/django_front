from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import async_proxy_request
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django_prometheus import exports
from asgiref.sync import sync_to_async

# Prometheus метрики
PROXY_REQUESTS = exports.Counter(
    'proxy_requests_total',
    'Total proxy requests',
    ['method', 'status']
)
REQUEST_TIME = exports.Histogram(
    'proxy_request_time_seconds',
    'Time spent processing proxy requests'
)


class AsyncProxyView(APIView):
    """Асинхронный прокси-класс"""

    async def dispatch(self, request, *args, **kwargs):
        start_time = time.time()
        response = await super().dispatch(request, *args, **kwargs)

        # Записываем метрики
        REQUEST_TIME.observe(time.time() - start_time)
        PROXY_REQUESTS.labels(
            method=request.method,
            status=response.status_code
        ).inc()

        return response

    async def get(self, request, path=''):
        data, from_cache = await async_proxy_request(request, path)
        return Response(
            data,
            headers={'X-Cache-Hit': str(from_cache)}
        )

    async def post(self, request, path=''):
        data, _ = await async_proxy_request(request, path)
        return Response(data)

    # Аналогично для PUT, PATCH, DELETE


class AsyncTokenObtainPairView(TokenObtainPairView):
    """Асинхронная выдача JWT токенов"""

    async def post(self, request, *args, **kwargs):
        return await sync_to_async(super().post)(request, *args, **kwargs)


class AsyncTokenRefreshView(TokenRefreshView):
    """Асинхронное обновление токенов"""

    async def post(self, request, *args, **kwargs):
        return await sync_to_async(super().post)(request, *args, **kwargs)