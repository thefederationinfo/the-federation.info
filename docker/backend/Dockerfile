FROM python:3.6

ENV PYTHONUNBUFFERED 1

COPY requirements/requirements.txt ./
RUN pip install -U pip setuptools pip-tools
RUN pip-sync requirements.txt

RUN mkdir -p /logs

RUN groupadd -r django \
    && useradd -r -g django django

COPY . /app

RUN chown -R django /app

#COPY docker/backend/uwsgi.ini /app/config/uwsgi.ini
COPY docker/backend/gunicorn.sh /gunicorn.sh
COPY docker/backend/entrypoint.sh /entrypoint.sh

RUN sed -i 's/\r//' /entrypoint.sh \
    && sed -i 's/\r//' /gunicorn.sh \
    && chmod +x /entrypoint.sh \
    && chown django /entrypoint.sh \
    && chmod +x /gunicorn.sh \
    && chown django /gunicorn.sh

WORKDIR /app

ENV RQWORKER_NUM 5
#ENV VIRTUAL_ENV /usr/local
#ENV THEFEDERATION_HOME /app
ENV DJANGO_SETTINGS_MODULE config.production
ENV REDIS_HOST redis
ENV DATABASE_URL postgres://postgres:postgres@db:5432/postgres
ENV DJANGO_SECURE_SSL_REDIRECT False
ENV DJANGO_DEBUG True
ENV ALLOWED_HOSTS federation.local

EXPOSE 5000

ENTRYPOINT ["/entrypoint.sh"]
