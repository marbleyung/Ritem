FROM python:3.10-alpine

WORKDIR /Ritem

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY reqs.txt .

RUN apk add --no-cache postgresql-client build-base postgresql-dev gcc \
	libc-dev linux-headers && mkdir /Ritem/static_cdn
RUN pip install --upgrade pip && pip install --no-cache-dir -r reqs.txt


COPY entrypoint.sh .
RUN sed -i 's/\r$//g' /Ritem/entrypoint.sh && chmod +x /Ritem/entrypoint.sh

COPY . .

ENTRYPOINT ["/Ritem/entrypoint.sh"]
