FROM python:3.11-slim
LABEL maintainer="Ilgiz Rakhimianov <i@rakhimianov.ru>"

ARG DEPENDENCIES="curl vim postgresql-client"
RUN apt-get update && apt-get install -y $DEPENDENCIES

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /opt/app
WORKDIR /opt/app

ARG POETRY_VERSION="1.7.1"
RUN pip install poetry==$POETRY_VERSION
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

EXPOSE 80

VOLUME /media/
VOLUME /static/

CMD rm -rf static; \
    rm -rf media; \
    python3 ./manage.py migrate; \
    python3 ./manage.py collectstatic --noinput;\
    python3 ./manage.py runserver 0.0.0.0:8000