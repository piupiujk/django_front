import json

import requests
from django.conf import settings

FASTAPI_BASE_URL = getattr(settings, 'FASTAPI_BASE_URL', 'http://document_app:8000').strip('/')



def call_fastapi(endpoint: str, method: str = 'get', data: dict = None):
    url = f"{FASTAPI_BASE_URL}/{endpoint}".strip('/')

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    json_data = json.dumps(data)

    try:
        response = requests.request(
            method.upper(),
            url,
            data=json_data,
            headers=headers
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}\nResponse: {e.response.text if e.response else 'No response'}")
        return None