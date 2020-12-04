FROM python:3.8-slim-buster

# without being first buffered
# https://stackoverflow.com/questions/59812009/what-is-the-use-of-pythonunbuffered-in-docker-file
ENV PYTHONUNBUFFERED 1
# Disabling Bytecode (.pyc) Files
# https://python-docs.readthedocs.io/en/latest/writing/gotchas.html
#ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir /code/
WORKDIR /code/

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Translations dependencies
  && apt-get install -y gettext \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install -r /requirements/local.txt

COPY --chown=local_web_phuot:local_web_phuot ./docker/local/web_phuot/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

ADD . /code/

EXPOSE 80
CMD exec uwsgi --http :80 --module config.wsgi
