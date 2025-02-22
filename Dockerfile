FROM python:3.7-alpine

COPY requirements.txt requirements.txt
RUN apk update && \
    apk add --virtual build-deps gcc musl-dev && \
    apk add postgresql-dev && \
    rm -rf /var/cache/apk/*

RUN pip install -r requirements.txt

# delete dependencies required to install certain python packages 
# so the docker image size is low enough for Zeit now
RUN apk del build-deps gcc musl-dev

COPY . /app
WORKDIR /app

ENV FLASK_ENV=prod

EXPOSE 5000
ENTRYPOINT [ "gunicorn", "-b", "0.0.0.0:5000", "--log-level", "INFO", "manage:app" ]