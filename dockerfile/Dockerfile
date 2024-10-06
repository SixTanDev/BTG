# Base image for Ubuntu
FROM ubuntu:latest
LABEL authors="sixtandev"

# Use Python 3.10 as the base image
FROM python:3.10

# Install Poetry package manager
RUN pip install poetry

# Configure Poetry to install dependencies directly to the system (no virtualenv)
RUN poetry config virtualenvs.create false

# Maintainer of the image
MAINTAINER sixtandev@gmail.com

# Keeps the container running indefinitely
# CMD ["tail", "-f", "/dev/null"]
