FROM ubuntu:latest
LABEL authors="sixtandev"

FROM python:3.10

RUN pip install poetry

# Configure Poetry to install dependencies directly to the system (no virtualenv)
RUN poetry config virtualenvs.create false

WORKDIR /server
COPY .env /server

# Maintainer of the image
MAINTAINER sixtandev@gmail.com
