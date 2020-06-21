FROM python:3.7

MAINTAINER Shakhmaev Evgeny

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

# Install dependencies
COPY Pipfile /code/
RUN pip install pipenv
RUN pipenv lock && pipenv install --system

# Copying is disabled so that live updates can work
# Copy project
#COPY . /code/