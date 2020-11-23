FROM python:3.9-alpine

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

# Install postgres client
RUN apk add --update --no-cache postgresql-client jpeg-dev

# Install individual dependencies
# so that we could avoid install extra packages
RUN apk add --update --no-cache --virtual .tmp-build-deps \
      gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
RUN pip install -r /requirements.txt

# Remove dependencies
RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app

# Add media volume and static dirs
RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

# [Security] Limit the scope of user who run the docker image
RUN adduser -D user

# Give user permission to access static directories
# -R is for recursive, meaning setting permission for all sub-dirs of /vol
RUN chown -R user:user /vol/

# Allow everyone to read and execute
# the owner is allowed to write to as well
RUN chmod -R 755 /vol/web

USER user