FROM python:alpine
MAINTAINER HelloLily

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN rm requirements.txt

WORKDIR /usr/src/slackbot
