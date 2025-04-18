import aiohttp
import json
import time
from jose import jwt, JWTError
from django.conf import settings
from asgiref.sync import sync_to_async
from aioredis import Redis
from django.core.cache import caches


async def get_redis() -> Redis:
    return await caches['default'].client.get_client()


async def async_proxy_request(request, path=''):
    """Асинхронное проксирование запроса"""
    start_time = time.time()
    redis = await get_redis()
    cache_key = f"proxy:{request.method}:{path}:{hash(frozenset(request.GET.items()))}"

    # Пробуем получить из кеша
    if request.method == 'GET':
        cached = await redis.get(cache_key)
        if cached:
            await save_log_async({
                **extract_request_data(request, start_time),
                'response_body': cached.decode(),
                'from_cache': True,
                'target_url': f"{settings.PROXY_CONFIG['FASTAPI_URL']}/{path}",
            })
            return json.loads(cached), True

    # Делаем запрос к FastAPI
    async with aiohttp.ClientSession() as session:
        async with session.request(
                method=request.method,
                url=f"{settings.PROXY_CONFIG['FASTAPI_URL']}/{path}",
                headers={k: v for k, v in request.headers.items() if k.lower() not in ['host']},
                data=await request.body(),
                params=request.GET,
        ) as response:
            response_text = await response.text()

            # Кешируем GET-запросы
            if request.method == 'GET' and response.status == 200:
                await redis.setex(
                    cache_key,
                    settings.PROXY_CONFIG['CACHE_TIMEOUT'],
                    response_text
                )

            await save_log_async({
                **extract_request_data(request, start_time),
                'status_code': response.status,
                'response_headers': dict(response.headers),
                'response_body': response_text,
                'from_cache': False,
                'target_url': f"{settings.PROXY_CONFIG['FASTAPI_URL']}/{path}",
            })

            return json.loads(response_text) if 'application/json' in response.headers.get('Content-Type',
                                                                                           '') else response_text, False


async def save_log_async(log_data):
    """Асинхронное сохранение лога"""
    from .models import ProxyLog
    await sync_to_async(ProxyLog.objects.create)(**log_data)


def extract_request_data(request, start_time):
    """Извлечение данных из запроса"""
    return {
        'user_id': request.user.id if request.user.is_authenticated else None,
        'ip_address': get_client_ip(request),
        'method': request.method,
        'path': request.get_full_path(),
        'request_headers': dict(request.headers),
        'request_body': request.body.decode() if request.body else None,
        'response_time': time.time() - start_time,
    }


def get_client_ip(request):
    """Получение IP клиента"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')