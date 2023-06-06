FROM python:3.10-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

RUN adduser --disabled-password ritem-user && \
    apk add --no-cache postgresql-client build-base postgresql-dev gcc libc-dev linux-headers && \
    pip install --no-cache-dir -r reqs.txt

EXPOSE 8000
