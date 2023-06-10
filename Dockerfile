FROM python:3.10-alpine

WORKDIR /Ritem

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY reqs.txt .

RUN apk add --no-cache postgresql-client build-base postgresql-dev gcc \
	libc-dev linux-headers
RUN python -m venv /venv && source /venv/bin/activate && \
	pip install --upgrade pip && pip install --no-cache-dir -r reqs.txt

COPY . .
