FROM python:3.7.3-alpine

# without being first buffered
# https://stackoverflow.com/questions/59812009/what-is-the-use-of-pythonunbuffered-in-docker-file
ENV PYTHONUNBUFFERED 1
# Disabling Bytecode (.pyc) Files
# https://python-docs.readthedocs.io/en/latest/writing/gotchas.html
#ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir /code/
WORKDIR /code/

#RUN apk add && apk update \
#  # dependencies for building Python packages
#  && apk install -y build-essential \
#  # mysql dependencies
#  && apk add mysql-client \
#  # cleaning up unused files
#  && apk purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
#  && rm -rf /var/lib/apk/lists/*

RUN apk update \
    && apk add --virtual build-dependencies
    build-base
    gcc
    wget
    git
    mysql-client

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install -r --no-cache-dir /requirements/requirements.txt

ADD . /code/
