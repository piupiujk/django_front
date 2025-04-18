#!/bin/bash

python manage.py migrate
python manage.py runserver 0.0.0.0:${DOCKER_PORT} --noreload
daphne -b 0.0.0.0 -p 8000 docanalyser.asgi:application