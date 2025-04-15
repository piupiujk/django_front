FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

RUN apt update && apt -qy install gcc libjpeg-dev libpq-dev gettext \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /django_front

RUN mkdir static && mkdir media

COPY . .

RUN pip install -r requirements.txt

RUN chmod a+x /django_front/app.sh