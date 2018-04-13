FROM python:3

COPY requirements/requirements.txt ./
RUN pip install -U pip setuptools pip-tools
RUN pip-sync requirements.txt

RUN mkdir -p /logs

WORKDIR /app

COPY . /app

COPY docker/backend/uwsgi.ini /app/config/uwsgi.ini

# TODO do optimization with multi-container setup later once things all work
#FROM python:3.6-alpine3.7 AS alpinebase
#RUN apk update && apk add git postgresql-dev gcc python3-dev musl-dev libxml2-dev libxslt-dev g++
#COPY --from=dependencies /app/requirements.txt ./
#COPY --from=dependencies /root/.cache /root/.cache

ENV RQWORKER_NUM 5
ENV VIRTUAL_ENV /usr/local
ENV THEFEDERATION_HOME /app
ENV DJANGO_SETTINGS_MODULE config.production
ENV REDIS_HOST redis
ENV DATABASE_URL postgres://postgres:postgres@db:5432/postgres

EXPOSE 8000

CMD ["circusd", "/app/config/circus.ini"]
