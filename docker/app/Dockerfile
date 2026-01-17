FROM docker.io/library/python:3.9 AS geoip

ARG MAXMIND_LICENSE_KEY
RUN wget "https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-Country&license_key=${MAXMIND_LICENSE_KEY}&suffix=tar.gz" -O /geoip.tar.gz

FROM docker.io/library/python:3.9

ENV PYTHONUNBUFFERED=1

COPY requirements/requirements.txt /requirements.txt

RUN apt-get update -qq && apt-get install python-dev-is-python3 python3-dev -qqy
RUN pip install --no-cache-dir setuptools pip-tools
RUN pip-sync requirements.txt

RUN groupadd -r django \
    && useradd -r -g django django

COPY --chown=django:django . /app
COPY --chown=django:django docker/app/gunicorn.sh /gunicorn.sh

COPY --from=geoip /geoip.tar.gz /tmp/geoip.tar.gz
RUN tar xva -C /app/utils/maxmind --overwrite --strip-components 1 -f /tmp/geoip.tar.gz

ENV POSTGRES_PASSWORD=postgres
ENV RQWORKER_NUM=5
ENV DJANGO_SETTINGS_MODULE=config.production
ENV REDIS_HOST=redis
ENV DATABASE_URL=postgres://postgres:$POSTGRES_PASSWORD@db:5432/postgres
ENV DJANGO_SECURE_SSL_REDIRECT=True
ENV DJANGO_DEBUG=False
ENV DJANGO_ALLOWED_HOSTS=the-federation.info,dev.the-federation.info,thefederation.local
ENV DBHOST=db

WORKDIR /app
CMD bash -c "./utils/wait-for-it/wait-for-it.sh --strict --timeout=10 $DBHOST:5432 && circusd /app/config/circus.ini"
