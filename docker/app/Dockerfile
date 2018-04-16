# --------------------
# Build frontend first
# --------------------

FROM node:9 AS frontend

COPY . /app

WORKDIR /app

RUN npm i && npm run build

# -----------
# Backend
# -----------

FROM python:3.6

ENV PYTHONUNBUFFERED 1

COPY requirements/requirements.txt ./

RUN pip install -U pip setuptools pip-tools

RUN pip-sync requirements.txt

RUN mkdir -p /logs

RUN groupadd -r django \
    && useradd -r -g django django

COPY . /app

COPY --from=frontend /app/dist /app/frontend

COPY docker/app/gunicorn.sh /gunicorn.sh

RUN sed -i 's/\r//' /gunicorn.sh \
    && chmod +x /gunicorn.sh \
    && chown django /gunicorn.sh

WORKDIR /app

RUN chown -R django /app

ENV RQWORKER_NUM 5
ENV DJANGO_SETTINGS_MODULE config.production
ENV REDIS_HOST redis
ENV DATABASE_URL postgres://postgres:postgres@db:5432/postgres
ENV DJANGO_SECURE_SSL_REDIRECT True
ENV DJANGO_DEBUG False
ENV DJANGO_ALLOWED_HOSTS the-federation.info,dev.the-federation.info,thefederation.local

CMD circusd /app/config/circus.ini
