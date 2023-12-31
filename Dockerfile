FROM python:3.10-alpine
WORKDIR /usr/
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt /usr/requirements.txt
RUN set -eux \
    && apk add --no-cache --virtual .build-deps build-base \
        libressl-dev libffi-dev gcc musl-dev python3-dev \
        sqlite \
    && pip install --upgrade pip setuptools wheel \
    && pip install -r /usr/requirements.txt \
    && rm -rf /root/.cache/pip
COPY . /usr/