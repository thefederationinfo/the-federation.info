FROM python:3

# Ensure pip and setuptools are up to date as well
RUN pip install -U pip setuptools pip-tools

RUN mkdir -p /code

COPY . /code/

WORKDIR /code

RUN pip-sync requirements.txt

# For uWSGI
EXPOSE 8000

CMD circus config/circus.ini
