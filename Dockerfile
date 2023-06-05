FROM python:3.10-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./reqs.txt .
RUN pip install -r reqs.txt --default-timeout=100

COPY . .
EXPOSE 8000
